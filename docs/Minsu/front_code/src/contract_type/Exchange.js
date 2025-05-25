// ExchangeContract.js
import React from "react";

function ExchangeContract({ contract }) {
  return (
    <>
      <h2>🔄 {contract.contract_type}</h2>
      <p><strong>계약일:</strong> {contract.contract_date}</p>

      <h3>🏘️ 갑 부동산 정보</h3>
      <p><strong>위치:</strong> {contract.property_A.location}</p>
      <p><strong>지목:</strong> {contract.property_A.land_category}</p>
      <p><strong>면적:</strong> {contract.property_A.land_area}</p>
      <p><strong>건물 정보:</strong> {contract.property_A.building_details}</p>

      <h3>🏘️ 을 부동산 정보</h3>
      <p><strong>위치:</strong> {contract.property_B.location}</p>
      <p><strong>지목:</strong> {contract.property_B.land_category}</p>
      <p><strong>면적:</strong> {contract.property_B.land_area}</p>
      <p><strong>건물 정보:</strong> {contract.property_B.building_details}</p>

      <h3>🙋‍♂️ 갑 당사자</h3>
      <p><strong>성명:</strong> {contract.party_A.name}</p>
      <p><strong>주민등록번호:</strong> {contract.party_A.id_number}</p>
      <p><strong>주소:</strong> {contract.party_A.address}</p>
      <p><strong>연락처:</strong> {contract.party_A.contact}</p>

      <h3>🙋‍♀️ 을 당사자</h3>
      <p><strong>성명:</strong> {contract.party_B.name}</p>
      <p><strong>주민등록번호:</strong> {contract.party_B.id_number}</p>
      <p><strong>주소:</strong> {contract.party_B.address}</p>
      <p><strong>연락처:</strong> {contract.party_B.contact}</p>

      <h3>💰 교환 차액 지급</h3>
      <p><strong>총액:</strong> {contract.exchange_payment.total_price}</p>
      <p><strong>계약금:</strong> {contract.exchange_payment.down_payment.amount} (지급일: {contract.exchange_payment.down_payment.payment_date})</p>
      <p><strong>중도금:</strong> {contract.exchange_payment.interim_payment.amount} (지급일: {contract.exchange_payment.interim_payment.payment_date})</p>
      <p><strong>잔금:</strong> {contract.exchange_payment.balance_payment.amount} (지급일: {contract.exchange_payment.balance_payment.payment_date})</p>

      <h3>📄 소유권 이전</h3>
      <p><strong>서류 이전일:</strong> {contract.ownership_transfer.document_transfer_date}</p>
      <p><strong>부동산 인도일:</strong> {contract.ownership_transfer.property_delivery_date}</p>

      <h3>❌ 계약 해제</h3>
      <p><strong>위약금:</strong> {contract.termination.penalty_amount}</p>

      <h3>🏢 중개사 정보</h3>
      <p><strong>중개사무소 명칭:</strong> {contract.broker.office_name}</p>
      <p><strong>주소:</strong> {contract.broker.office_address}</p>
      <p><strong>대표자:</strong> {contract.broker.representative}</p>
      <p><strong>등록번호:</strong> {contract.broker.registration_number}</p>
      <p><strong>담당 중개사:</strong> {contract.broker.broker_name}</p>

      <h3>📝 특약사항</h3>
      <p>{contract.special_terms}</p>

      <h3>✍️ 서명 및 날인</h3>
      <p>{contract.signature_and_seal}</p>
    </>
  );
}

export default ExchangeContract;