# {{contract_name}}

**사업주(회사명)** : {{employer.company_name}}  
대표자 성명 : {{employer.representative_name}}  
사업장 주소 : {{employer.address}}  
연락처 : {{employer.contact}}

**근로자 성명** : {{employee.name}}  
주민등록번호 : {{employee.resident_number}}  
주소 : {{employee.address}}  
연락처 : {{employee.contact}}

---

### 1. 근로조건

- 직책 : {{employment_details.position}}  
- 업무 내용 : {{employment_details.duties}}  
- 근무 장소 : {{employment_details.workplace}}  
- 계약기간 : {{employment_details.contract_period.start_date}} ~ {{employment_details.contract_period.end_date}}  
- 근무일 : {{employment_details.working_days}}  
- 근무시간 : {{employment_details.working_hours.start_time}} ~ {{employment_details.working_hours.end_time}} (휴게시간: {{employment_details.working_hours.break_time}})

---

### 2. 임금

- 임금형태 : {{wage_details.wage_type}}  
- 금액 : {{wage_details.wage_amount}}원  
- 지급일 : 매월 {{wage_details.payment_date}}일  
- 지급방법 : {{wage_details.payment_method}}

---

### 3. 휴일 및 휴가

{{holidays}}

---

### 4. 4대보험 가입

- 국민연금 : {{social_insurance.national_pension}}  
- 건강보험 : {{social_insurance.health_insurance}}  
- 고용보험 : {{social_insurance.employment_insurance}}  
- 산재보험 : {{social_insurance.industrial_accident_insurance}}

---

### 5. 계약 해지 및 기타사항

- {{termination}}  
- {{other_terms}}

---

000(이하 '갑'이라 칭함)와 000(이하 '을'이라 칭함)은 상기 계약 내용에 합의하고, 아래와 같이 계약서를 작성합니다.

계약일 : {{contract_date}}

**사업주 서명** : ___________________  
**근로자 서명** : ___________________