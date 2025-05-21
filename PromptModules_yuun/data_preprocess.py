import os
import whisper
from hanspell import spell_checker
from pyannote.audio import Pipeline
from pyannote.core import Segment
import nltk
from nltk.corpus import stopwords
import re

from dotenv import load_dotenv, find_dotenv

# 파일 로드
## data_preprocess.py와 동일한 디렉토리 내에 있다고 가정함
def load_file(fs, nfile):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 절대 경로 기준
    path = os.path.join(base_dir, fs, nfile)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"파일 없음: {path}")
    
    return path

# 음성 추출 및 화자 분리
def diarized_transcription(audio_nfile, txt_nfile):
    audio_path=load_file("user_data", audio_nfile)
    
    # Whisper로 텍스트 전사
    model=whisper.load_model("large")  
    result = model.transcribe(audio_path)
    
    # pyannote.audio로 화자 분리
    # 화자는 두 명으로 지정
    # HUGGINGFACE_TOKEN
    _=load_dotenv(find_dotenv())
    hf_token= os.getenv("HUGGINGFACE_TOKEN")

    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)
    except Exception as e:
        raise RuntimeError(f"❌ pyannote pipeline 로드 실패: {e}")
    
    diarization=pipeline(audio_path, num_speakers=2)
    transcript = result["segments"]
    
    # diarization 결과에서 각 타임슬롯과 화자 정보를 가져옴
    diarized_output = []
    for seg in transcript:
        whisper_start = seg["start"]
        whisper_end = seg["end"]
        whisper_segment = Segment(whisper_start, whisper_end)
        matched_speaker = None
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            diarized_segment = Segment(turn.start, turn.end)  
            if whisper_segment.overlaps(diarized_segment):
                matched_speaker = speaker
                break  # 첫 번째 매칭된 화자만 사용

        if matched_speaker:
            diarized_output.append(f"{matched_speaker}: {seg['text'].strip()}")
                    
    # 텍스트 파일로 저장
    with open(txt_nfile, "w", encoding="utf-8") as f:
        for line in diarized_output:
            f.write(line + "\n")
            
            
# nltk 불용어 다운로드
## nltk는 한국어 불용어를 제공하지 않음
## 따로 불용어 리스트를 txt 파일로 지정해둠
nltk.download('stopwords')
def load_stopwords_from_file(nfile):
    sw_path = load_file("stopwords", nfile)
    
    with open(sw_path, 'r', encoding='utf-8') as f:
        stopwords_list = [line.strip() for line in f if line.strip()]
    return set(stopwords_list)

# 한글/공백만 남기고 정제
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^가-힣\s]', '', text)
    return text

# 텍스트 전처리
def data_preprocess(input_txt_nfile, output_txt_nfile, stopwords_nfile):
    # 불용어 목록 불러오기
    stop_words = load_stopwords_from_file(stopwords_nfile)
    
    with open(input_txt_nfile, "r", encoding="utf-8") as f:
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
    ### words_token으로 변경 하여 토큰화 할 수 있음
    words = clean_text(corrected).split()
    filtered = [word for word in words if word not in stop_words]
    processed_text = " ".join(filtered)
    
    # 결과 저장
    with open(output_txt_nfile, "w", encoding="utf-8") as f:
        f.write(processed_text)
        

def main(): 
    audio_nfile = "audio_input.wav"
    diarized_txt_nfile= "diarized_output.txt"
    processed_txt_nfile= "processed_output.txt"
    stopwords_nfile="korean_stopwords.txt"
    
    # 오디오 변환
    diarized_transcription(audio_nfile, diarized_txt_nfile)
    
    # 텍스트 전처리
    data_preprocess(diarized_txt_nfile,processed_txt_nfile, stopwords_nfile)
    
    # 원본 삭제
    os.remove(diarized_txt_nfile)
    os.remove(audio_nfile)
    
if __name__=="__main__":
    main()
    