import os
import whisper
from pyannote.audio import Pipeline
import librosa
import soundfile as sf

from hanspell import spell_checker
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from dotenv import load_dotenv, find_dotenv

# 파일 로드
def load_file(fs, nfile, create_dir=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로 기준
    dir_path = os.path.join(base_dir, fs)
    path = os.path.join(dir_path, nfile)
    
    # 디렉토리가 없으면 생성
    if create_dir and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"디렉토리 생성: {dir_path}")
    
    # 읽기 모드에서는 파일 존재 확인
    if not create_dir and not os.path.exists(path):
        raise FileNotFoundError(f"파일 없음: {path}")
    
    return path

# 화자 분리 및 음성 추출 매칭
def diarized_transcription(audio_nfile, txt_nfile):
    audio_path=load_file("user_data", audio_nfile)
    txt_path = load_file("user_data", txt_nfile, create_dir=True)
    
    # 1. pyannote.audio로 화자 분리
    # 화자는 두 명으로 지정
    # HUGGINGFACE_TOKEN
    _=load_dotenv(find_dotenv())
    hf_token= os.getenv("HUGGINGFACE_TOKEN")

    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)
    except Exception as e:
        raise RuntimeError(f"❌ pyannote pipeline 로드 실패: {e}")
    
    diarization=pipeline(audio_path, num_speakers=2)
    
    # 2. 오디오 파일 로드 (세그먼트 추출용)
    audio_data, sr = librosa.load(audio_path, sr=16000)
    
    # 3. Whisper 모델 로드
    model=whisper.load_model("medium") 
     
    # 4. 화자별 세그먼트 그룹화 및 병합
    all_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        all_segments.append({
            'start': turn.start,
            'end': turn.end,
            'speaker': speaker
        })
        
    all_segments.sort(key=lambda x:x['start'])
    
    # 짧은 음성 세그먼트들을 병합하여 음성 인식 정확도 향상
    def merge_short_segments(segments, min_duration=1.0, max_gap=0.5):
        if not segments:
            return segments
        
        merged = []
        current_segment = segments[0].copy()
        
        for next_segment in segments[1:]:
            # 같은 화자이고, 간격이 작고, 현재 세그먼트가 짧은 경우 병합
            gap = next_segment['start'] - current_segment['end']
            current_duration = current_segment['end'] - current_segment['start']
            
            if (current_segment['speaker'] == next_segment['speaker'] and 
                gap <= max_gap and 
                current_duration < min_duration):
                current_segment['end'] = next_segment['end']
            else:
                merged.append(current_segment)
                current_segment = next_segment.copy()
        merged.append(current_segment)
        
        return merged

    all_segments=merge_short_segments(all_segments, min_duration=1.0, max_gap=0.5)
    
    # 5. 각 화자별로 음성 인식
    diarized_output = []
    
    for i, segment in enumerate(all_segments):
        start_time = segment['start']
        end_time = segment['end']
        speaker = segment['speaker']
        
        # 시간을 샘플 인덱스로 변환
        start_sample = int(start_time * sr)
        end_sample = int(end_time * sr)
            
        # 범위 검증
        start_sample = max(0, start_sample)
        end_sample = min(len(audio_data), end_sample)
            
        if start_sample >= end_sample:
            continue
        
        segment_audio = audio_data[start_sample:end_sample]
    
        # 임시 파일로 저장 (whisper 입력용)
        temp_audio_path = f"temp_segment_{i}_{speaker}.wav"
        sf.write(temp_audio_path, segment_audio, sr)
        
        try:
            # Whisper로 음성 인식
            result = model.transcribe(temp_audio_path, language='ko')
            if result["segments"]:
                # 전체 텍스트 사용
                ## 세그먼트별 시간 정보는 임시 파일 기준이므로 부정확함
                full_text = result["text"].strip()
                if full_text:
                    diarized_output.append({
                        'speaker': speaker,
                        'text': full_text,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time
                    }) 
        except Exception as e:
            print(f"⚠️ {speaker} 음성 인식 실패: {e}")
        finally:
            # 임시 파일 정리
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    
    # 6. 결과 정렬 및 저장 (첫 번째 발화 시간 기준)
    diarized_output.sort(key=lambda x: x['start_time'])
                    
    # 텍스트 파일로 저장
    with open(txt_path, "w", encoding="utf-8") as f:
        for item in diarized_output:
            speaker = item['speaker']
            text = item['text']
            # 화자별 발화 시간 정보 포함
            f.write(f"{speaker}: {text}\n")
            
            
# nltk 불용어 다운로드
## nltk는 한국어 불용어를 제공하지 않음
## 따로 불용어 리스트를 txt 파일로 지정해둠
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# 텍스트 전처리
def text_preprocess(input_txt_nfile, output_txt_nfile, stopwords_nfile):
    def load_stopwords_from_file(nfile):
        sw_path = load_file("stopwords", nfile)
        
        with open(sw_path, 'r', encoding='utf-8') as f:
            stopwords_list = [line.strip() for line in f if line.strip()]
        return set(stopwords_list)

    # 불용어 목록 불러오기
    stop_words = load_stopwords_from_file(stopwords_nfile)
    # 입력 파일 경로 (user_data 디렉토리에서 읽기)
    input_path = load_file("user_data", input_txt_nfile)
    # 출력 파일 경로 (user_data 디렉토리에 저장)
    output_path = load_file("user_data", output_txt_nfile, create_dir=True)
    
    with open(input_path, "r", encoding="utf-8") as f:
        original_text = f.read()
        
    # 맞춤법 교정
    ### KeyError 예외 처리 및 큰 텍스트 분할 처리
    try:
        # 긴 텍스트는 여러 청크로 나누어 처리
        chunk_size = 500  # 한 번에 처리할 최대 글자 수
        chunks = [original_text[i:i+chunk_size] for i in range(0, len(original_text), chunk_size)]
        
        corrected_chunks = []
        for chunk in chunks:
            try:
                # 각 청크에 대해 맞춤법 검사 수행
                corrected_chunk = spell_checker.check(chunk)
                corrected_chunks.append(corrected_chunk.checked)
            except KeyError:
                # KeyError가 발생하면 원래 청크를 사용
                print(f"맞춤법 검사 중 KeyError 발생, 원문 사용: {chunk[:30]}...")
                corrected_chunks.append(chunk)
            except Exception as e:
                # 기타 예외 처리
                print(f"맞춤법 검사 중 예외 발생: {e}")
                corrected_chunks.append(chunk)
                
        corrected = ' '.join(corrected_chunks)
    except Exception as e:
        print(f"맞춤법 검사 전체 과정 중 오류 발생: {e}")
        corrected = original_text  # 오류 발생 시 원본 텍스트 사용
    
    # 불용어 제거
    ## words_token으로 변경 하여 토큰화
    word_tokens=word_tokenize(corrected)
    filtered = [word for word in word_tokens if word not in stop_words]
    processed_text = " ".join(filtered)
    
    # 결과 저장
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(processed_text)
        

def data_preprocess(): 
    # audio_nfile = "audio_input.wav"
    audio_nfile = "test_audio.wav"
    diarized_txt_nfile= "diarized_output.txt"
    processed_txt_nfile= "processed_output.txt"
    stopwords_nfile="korean_stopwords.txt"
    
    try:
        # 오디오 변환
        print("🎵 음성 인식 및 화자 분리 시작...")
        diarized_transcription(audio_nfile, diarized_txt_nfile)
        print("✅ 음성 인식 완료")
        
        # 텍스트 전처리
        print("📝 텍스트 전처리 시작...")
        text_preprocess(diarized_txt_nfile, processed_txt_nfile, stopwords_nfile)
        print("✅ 텍스트 전처리 완료")
        
        # 중간 파일 정리
        if os.path.exists(load_file("user_data", diarized_txt_nfile)):
            os.remove(load_file("user_data", diarized_txt_nfile))
            print("🗑️ 중간 파일 정리 완료")
        # if os.path.exists(load_file("user_data", audio_nfile)):
        #     os.remove(load_file("user_data", audio_nfile))
        #     print("🗑️ 중간 파일 정리 완료")
        
        print("🎉 모든 처리가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 처리 중 오류 발생: {e}")