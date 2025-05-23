# 발표 스크립트

안녕하세요. AI를 활용한 계약서 작성 자동화 프로젝트의 두 번째 발표를 맡은 김민석입니다.

## [1] 수행 배경 및 목표

보통 계약이라 하면 어떤 정해진 양식의 계약서를 작성하는 것을 떠올리시는 분이 많을 것 같은데요. 사실 법적으로는 말로만 진행하는 계약인 구두 계약도 녹음을 남기면 법적인 효력이 있습니다. 그렇지만 계약 내용을 문서 형태로 남기는 게 법적인 증명에 효율적이기 때문에, 대부분의 경우 당사자가 직접 또는 변호사와 같은 전문가의 도움으로 계약서를 작성하게 됩니다. 저희 프로젝트에서는 인공지능을 활용해서 구두 계약 음성을 바탕으로 계약서 초안을 생성하는 시스템을 개발해보고자 합니다. 저희의 핵심 목표는 이렇게 대화 음성으로 계약서를 생성하고, 또 생성된 계약서를 관리할 수 있는 웹 서비스를 개발하는 것입니다.

## [2] 전체 시스템 구조도

저희가 구현할 시스템을 전체적으로 한번 가볍게 살펴보겠습니다. 보시는 것처럼 크게 React 기반의 프론트엔드와 파이썬 기반의 백엔드로 구분됩니다. 사용자가 시스템에 로그인해서 대화 음성을 입력으로 주면, 백엔드에서는 OpenAI의 두 가지 API를 통해 이 음성을 분석하고 계약서를 생성합니다. 생성한 계약서는 내부 DB에 저장돼서 사용자가 이 문서를 웹상에서 편집하거나 PDF 형식으로 다운로드할 수 있습니다.

## [3] 시스템 모델 및 설계 (유스케이스, 동작, 구조)

### 3-1

사용자 관점에서 한번 시스템의 기능을 자세히 살펴보도록 하겠습니다. 우선 사용자가 시스템 자체 계정이나 네이버나 카카오 같은 소셜 계정으로 로그인합니다. 그리고 녹음 버튼을 누르고 당사자 간 대화를 진행하거나 미리 녹음해 둔 음성파일을 업로드합니다. 이 대화 음성은 Whisper API를 통해 텍스트 형태로 변환되고, 그 텍스트를 바탕으로 ChatGPT가 계약서 초안을 생성합니다. 또 여기 '공란 처리 및 제안' 기능을 보실 수 있는데,

### 3-2

이 기능의 필요성과 발표 뒷부분 내용을 이해하실 수 있도록 잠시 법률적인 배경을 간단하게 설명하겠습니다. 앞서 말씀드린 것처럼 대화 녹음이든 임의로 직접 만든 양식의 문서든, 당사자 간의 동의가 나타나고 그 내용이 법적으로 허용되는 범위라면 형식에 상관없이 효력이 발생합니다. 다만 임대차계약이나 고용계약처럼 계약 자체의 유형과 그 필수 요소는 법률에서 정형화된 경우가 많습니다. 이 경우에는 이런 필수 요소가 계약서에서 빠져 있으면 계약이 법적으로 인정되지 못할 수 있습니다.

### 3-3

대화 음성에서 이렇게 계약의 필수요소가 명확하게 나타나지 않으면, 계약서를 생성할 때 이 부분을 빈칸으로 표시하고 사용자에게 정보를 제안할 수도 있습니다. 근로계약으로 예를 들면, 급여가 확실하게 정해지지 않은 경우에 빈칸으로 두고 '2025년 최저임금은 시간당 10,030원입니다'와 같이 표시될 수 있습니다. 마지막으로 사용자는 이렇게 생성된 계약서를 웹 상에서 저장하고 불러와서 편집하거나 PDF로 다운로드할 수 있습니다.

### 3-4

이번에는 시스템 관점에서 동작 흐름을 따라가면서 다시 정리해보겠습니다. 먼저 사용자가 로그인하고 대화 음성을 업로드하면서 계약서 생성 요청이 발생합니다. 백엔드에서는 API 서버가 Whisper API를 호출해서 이 음성을 텍스트로 변환합니다. 그러면 텍스트 처리 모듈에서 이 텍스트를 전처리합니다. 구체적으로는 자연어 처리 라이브러리를 활용해서 띄어쓰기와 맞춤법 교정, 화자 분리, 불필요한 단어 제거 등의 과정을 거치면서 텍스트를 정제합니다. 이제 본격적으로 계약서를 생성하게 되는데요. 생성 로직을 크게 '텍스트 분석 및 계약 유형 판단', '키워드 추출 및 계약서 초안 생성', '누락 항목에 대한 법률 정보 제안'의 3단계로 나눴습니다. 각 단계마다 한 번 이상의 GPT API 호출을 거치게 되는데요, '프롬프트 생성 모듈'에서 GPT에 보낼 입력을 구성해서 GPT API를 호출하면 그 응답 텍스트를 '결과 가공 모듈'에서 다음 과정을 위해 파싱하는 과정을 반복하면서 진행됩니다. 이렇게 계약서가 생성되면 내부 DB에 저장되고 사용자 요청에 따라 불러오기, 편집, 저장이 이루어집니다.

## [4] 진행상황

### 4-1

저희는 본격적인 구현은 아직 제대로 시작하지는 않은 상태입니다. 지금 시점에서는 구현 작업에 들어갈 수 있도록 각자 역할에 따라 구체적인 설계를 진행하고 있고, 주로 Notion에 문서로 기록하고 공유하면서 진행하고 있습니다.

### 4-2

구체적으로 프롬프트 쪽에서는 우선 텍스트 전처리와 가공을 위해 자연어 처리 라이브러리를 조사해보고 구현에 어떻게 적용할 지에 대한 전략을 문서화했습니다. 그리고 계약 관련 실제 데이터셋을 조사하고 분석해서 구현 과정에서 어떻게 활용할 지에 대한 전략도 정리했습니다. 가장 최근에는 국내 민법에서 정의하는 계약의 15가지 유형을 중심으로 법률을 조사해봤는데요. 조사한 내용을 바탕으로 이렇게 계약 유형별 키워드와 계약서 템플릿을 정형화하고 그에 맞는 프롬프트를 구성해 보면서 계약서 자동 생성이 가능한 구조를 설계해보고 있습니다.

### 4-3

프론트엔드에서는 화면 구성과 인터페이스 설계를 진행하고 있습니다. 종프1 때 기업측에서 '화면설계서'라는 기술문서 작성을 요구했었는데, 이번 기업측에서는 특별히 요구한 건 아니지만 종프1 때의 화면설계서 양식을 활용해서 이렇게 문서화해보고 있습니다. 보시다시피 각 요소에 대해 화면 경로, 기능에 대한 설명, 구현 시의 유의사항을 정의하면서 실제 구현에 이어지는 데 도움이 많이 될 것으로 생각합니다.

### 4-4

백엔드에서는 앞서 보셨던 그림과 비슷하게 전체 시스템의 구성과 요청 흐름을 구체화했습니다. 뒤의 이슈사항에서 자세히 말씀드리겠지만, 계획발표 이후에 요구사항에 변동이 있어서 시스템을 전반적으로 다시 설계하는 과정이 필요했습니다. 또 주제 특성상 데이터가 개인정보를 많이 포함할 수 있고 요구사항이 확대되면서 보안을 고려할 필요가 있어서, 보안 계층을 추가적으로 학습하고 검토하면서 시스템 설계에 적용하고 있는 중입니다.

## [5] 이슈사항 및 해결방안

이슈사항으로는 요구사항 확장과 그에 따른 프로젝트 범위 변동이 있는데요. 지난 계획발표 시점까지의 프로젝트 범위는 로그인이나 사용자 기능 없이, 대화 음성으로 계약서를 생성하고 다운로드할 수 있는 정도만 포함하는 웹 페이지였습니다. 이때의 핵심 과제는 이 계약서 생성 프로세스에 관한 프롬프트 엔지니어링에 최대한 집중하는 것이었습니다. 하지만 계획발표 이후 멘토님과의 회의 과정에서 사용자 로그인과 생성한 계약서에 대한 관리 기능과 같은 요구사항도 추가되었습니다. 그래서 구현해야 할 시스템의 범위가 넓어지면서 DB와 보안 계층을 추가적으로 고려해서 다시 전체적인 시스템을 설계해야 했습니다. 그리고 세부적인 역할 분담이나 전반적인 계획도 검토해보고 약간의 조정을 하게 되었습니다. 지금은 앞서 말씀드렸듯 이런 변동사항을 반영해서 설계 기간을 처음에 계획한 것보다 조금 더 길게 진행하면서 구현에 무리가 없도록 하는 과정에 있습니다.

## [6] 향후 일정

마지막으로 앞으로의 전반적인 일정입니다. 중간고사 일정을 고려해서 일단 이번주 내에 최대한 현재 진행 중인 설계 작업을 마무리하려 하고 있습니다. 구체적으로는 API 명세, 계약서 DB 설계, 세부 모듈 및 필요한 함수 정의까지 진행할 예정입니다. 중간고사 이후에는 대략 2-3주 정도 본격적인 구현 작업에 집중할 계획입니다. 그리고 그 이후 5월 마지막 주까지는 기능 테스트와 성능 개선, 배포 작업을 진행하면서 마무리할 예정입니다.

제가 준비한 내용은 여기까지입니다. 감사합니다.