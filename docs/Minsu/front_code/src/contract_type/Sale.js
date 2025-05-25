import React from "react";

function Sale({ contract }) {
  return (
    <>
      <h2>🏠 {contract.contract_type}</h2>
      <p><strong>계약일:</strong> {contract.contract_date}</p>

      <h3>🔸 매도인 정보</h3>
      <p><strong>성명:</strong> {contract.seller.name}</p>
      <p><strong>주민등록번호:</strong> {contract.seller.id_number}</p>
      <p><strong>주소:</strong> {contract.seller.address}</p>
      <p><strong>연락처:</strong> {contract.seller.contact}</p>

      <h3>🔸 매수인 정보</h3>
      <p><strong>성명:</strong> {contract.buyer.name}</p>
      <p><strong>주민등록번호:</strong> {contract.buyer.id_number}</p>
      <p><strong>주소:</strong> {contract.buyer.address}</p>
      <p><strong>연락처:</strong> {contract.buyer.contact}</p>

      <h3>📍 부동산 정보</h3>
      <p><strong>위치:</strong> {contract.property.location}</p>
      <p><strong>지목:</strong> {contract.property.land_category}</p>
      <p><strong>면적:</strong> {contract.property.land_area}</p>
      <p><strong>건물 정보:</strong> {contract.property.building_details}</p>

      <h3>💰 매매 금액</h3>
      <p><strong>총액:</strong> {contract.sale_price.total_price}</p>
      <p><strong>계약금:</strong> {contract.sale_price.down_payment.amount} (지급일: {contract.sale_price.down_payment.payment_date})</p>
      <p><strong>중도금:</strong> {contract.sale_price.interim_payment.amount} (지급일: {contract.sale_price.interim_payment.payment_date})</p>
      <p><strong>잔금:</strong> {contract.sale_price.balance_payment.amount} (지급일: {contract.sale_price.balance_payment.payment_date})</p>

      <h3>🔁 소유권 이전</h3>
      <p><strong>서류 이전일:</strong> {contract.ownership_transfer.document_transfer_date}</p>
      <p><strong>부동산 인도일:</strong> {contract.ownership_transfer.property_delivery_date}</p>

      <h3>❌ 계약 해제</h3>
      <p><strong>위약금:</strong> {contract.termination.penalty_amount}</p>

      <h3>📝 특약사항</h3>
      <p>{contract.special_terms}</p>

      <h3>✍️ 서명 및 날인</h3>
      <p>{contract.signature_and_seal}</p>
    </>
  );
}

export default Sale;