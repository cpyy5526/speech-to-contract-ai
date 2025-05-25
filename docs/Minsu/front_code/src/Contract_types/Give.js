import React from "react";

function Give({ contract }) {
  return (
    <>
      <h2>🎁 {contract.contract_type}</h2>
      <p><strong>계약일:</strong> {contract.contract_date}</p>

      <h3>🔸 증여자 정보</h3>
      <p><strong>성명:</strong> {contract.donor.name}</p>
      <p><strong>주민등록번호:</strong> {contract.donor.id_number}</p>
      <p><strong>주소:</strong> {contract.donor.address}</p>
      <p><strong>연락처:</strong> {contract.donor.contact}</p>

      <h3>🔸 수증자 정보</h3>
      <p><strong>성명:</strong> {contract.donee.name}</p>
      <p><strong>주민등록번호:</strong> {contract.donee.id_number}</p>
      <p><strong>주소:</strong> {contract.donee.address}</p>
      <p><strong>연락처:</strong> {contract.donee.contact}</p>

      <h3>📦 증여 재산</h3>
      <p><strong>종류:</strong> {contract.gifted_property.type}</p>
      <p><strong>구체 내용:</strong> {contract.gifted_property.details.description}</p>
      <p><strong>면적/크기:</strong> {contract.gifted_property.details.area}</p>
      <p><strong>시가/평가액:</strong> {contract.gifted_property.details.current_value}</p>

      <h3>🚚 이전 사항</h3>
      <p><strong>이전 날짜:</strong> {contract.delivery_details.delivery_date}</p>
      <p><strong>이전 방식:</strong> {contract.delivery_details.delivery_method}</p>

      <h3>⚖️ 권리 및 의무</h3>
      <p><strong>기존 권리:</strong> {contract.rights_and_obligations.existing_rights}</p>
      <p><strong>수증자 의무:</strong> {contract.rights_and_obligations.obligations}</p>

      <h3>❌ 계약 해제 조건</h3>
      <p><strong>사유:</strong> {contract.termination_conditions.reasons}</p>
      <p><strong>절차:</strong> {contract.termination_conditions.procedure}</p>

      <h3>📝 특약사항</h3>
      <p>{contract.special_terms}</p>

      <h3>✍️ 서명 및 날인</h3>
      <p>{contract.signature_and_seal}</p>
    </>
  );
}

export default Give;