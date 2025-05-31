import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const SalePage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      seller: {
        name: getText("seller-name"),
        id_number: getText("seller-id"),
        address: getText("seller-address"),
        contact: getText("seller-contact"),
      },
      buyer: {
        name: getText("buyer-name"),
        id_number: getText("buyer-id"),
        address: getText("buyer-address"),
        contact: getText("buyer-contact"),
      },
      property: {
        location: getText("property-location"),
        land_category: getText("property-category"),
        land_area: getText("property-area"),
        building_details: getText("property-building"),
      },
      sale_price: {
        total_price: getText("price-total"),
        down_payment: {
          amount: getText("price-down"),
          payment_date: getText("date-down"),
        },
        interim_payment: {
          amount: getText("price-interim"),
          payment_date: getText("date-interim"),
        },
        balance_payment: {
          amount: getText("price-balance"),
          payment_date: getText("date-balance"),
        },
      },
      ownership_transfer: {
        document_transfer_date: getText("date-doc"),
        property_delivery_date: getText("date-delivery"),
      },
      termination: {
        penalty_amount: getText("penalty"),
      },
      special_terms: getText("special-terms-box"),
      signature_and_seal: getText("sign-seal"),
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <>
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type, suggestions)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date, suggestions)}</p>

      <p className="section-title">1. 계약 당사자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">매도인</td>
            <td>{renderField("seller-name", contract.seller?.name, suggestions)}</td>
            <td>{renderField("seller-id", contract.seller?.id_number, suggestions)}</td>
            <td>{renderField("seller-address", contract.seller?.address, suggestions)}</td>
            <td>{renderField("seller-contact", contract.seller?.contact, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">매수인</td>
            <td>{renderField("buyer-name", contract.buyer?.name, suggestions)}</td>
            <td>{renderField("buyer-id", contract.buyer?.id_number, suggestions)}</td>
            <td>{renderField("buyer-address", contract.buyer?.address, suggestions)}</td>
            <td>{renderField("buyer-contact", contract.buyer?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 부동산 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">소재지</td>
            <td colSpan="3">{renderField("property-location", contract.property?.location, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">지목</td>
            <td>{renderField("property-category", contract.property?.land_category, suggestions)}</td>
            <td className="gray">면적</td>
            <td>{renderField("property-area", contract.property?.land_area, suggestions)}㎡</td>
          </tr>
          <tr>
            <td className="gray">건물 내역</td>
            <td colSpan="3">{renderField("property-building", contract.property?.building_details, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 매매 대금</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">총액</td>
            <td colSpan="3">{renderField("price-total", contract.sale_price?.total_price, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">계약금</td>
            <td>{renderField("price-down", contract.sale_price?.down_payment?.amount, suggestions)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-down", contract.sale_price?.down_payment?.payment_date, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">중도금</td>
            <td>{renderField("price-interim", contract.sale_price?.interim_payment?.amount, suggestions)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-interim", contract.sale_price?.interim_payment?.payment_date, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">잔금</td>
            <td>{renderField("price-balance", contract.sale_price?.balance_payment?.amount, suggestions)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-balance", contract.sale_price?.balance_payment?.payment_date, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 소유권 이전</p>
      <p className="contract-clause">
        매매 부동산에 대한 서류 이전일은 {renderField("date-doc", contract.ownership_transfer?.document_transfer_date, suggestions)}, 부동산 인도일은 {renderField("date-delivery", contract.ownership_transfer?.property_delivery_date, suggestions)}로 한다.
      </p>

      <p className="section-title">5. 계약 해제</p>
      <p className="contract-clause">
        계약 해제 시 위약금은 {renderField("penalty", contract.termination?.penalty_amount, suggestions)} 원으로 한다.
      </p>

      <p className="section-title">6. 특약사항</p>
      <div className="special-terms-box">
        {renderField("special-terms-box", contract.special_terms, suggestions)}
      </div>

      <p className="section-title">7. 서명란</p>
        <p className="signature-block">
          본 계약의 내용을 확인하고 이에 동의하여 서명합니다.
        </p>

        <table className="contract-table" style={{ marginTop: "20px" }}>
          <tbody>
            <tr>
              <td className="gray">매도인</td>
              <td>{renderField("seller-sign", contract.seller?.name, suggestions)} (인)</td>
            </tr>
            <tr>
              <td className="gray">매수인</td>
              <td>{renderField("buyer-sign", contract.buyer?.name, suggestions)} (인)</td>
            </tr>
          </tbody>
        </table>

    </>
  );
});

export default SalePage1;
