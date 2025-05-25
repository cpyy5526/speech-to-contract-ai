import React from "react";

function LoanContract({ contract }) {
  return (
    <>
      <h2>💵 {contract.contract_type}</h2>
      <p><strong>계약일:</strong> {contract.contract_date}</p>

      <h3>💰 금액 정보</h3>
      <p><strong>금액(한글):</strong> {contract.loan_amount.amount_korean}</p>
      <p><strong>금액(숫자):</strong> {contract.loan_amount.amount_number}</p>

      <h3>👤 채권자(돈을 빌려준 사람)</h3>
      <p><strong>성명:</strong> {contract.creditor.name}</p>
      <p><strong>주민등록번호:</strong> {contract.creditor.id_number}</p>
      <p><strong>주소:</strong> {contract.creditor.address}</p>
      <p><strong>연락처:</strong> {contract.creditor.contact}</p>

      <h3>🧍 채무자(돈을 빌린 사람)</h3>
      <p><strong>성명:</strong> {contract.debtor.name}</p>
      <p><strong>주민등록번호:</strong> {contract.debtor.id_number}</p>
      <p><strong>주소:</strong> {contract.debtor.address}</p>
      <p><strong>연락처:</strong> {contract.debtor.contact}</p>

      <h3>📈 이자 조건</h3>
      <p><strong>이자율:</strong> {contract.interest.rate}</p>
      <p><strong>이자 지급 방식:</strong> {contract.interest.payment_method}</p>
      <p><strong>이자 지급일:</strong> {contract.interest.payment_date}</p>

      <h3>📆 원금 상환</h3>
      <p><strong>상환일:</strong> {contract.repayment.repayment_date}</p>
      <p><strong>상환 방식:</strong> {contract.repayment.repayment_method}</p>
      <p><strong>상환 장소:</strong> {contract.repayment.repayment_location}</p>
      <p><strong>계좌 정보:</strong> {contract.repayment.account_info}</p>

      <h3>📝 특약사항</h3>
      <p>{contract.special_terms}</p>

      <h3>✍️ 서명 및 날인</h3>
      <p>{contract.signature_and_seal}</p>
    </>
  );
}

export default LoanContract;