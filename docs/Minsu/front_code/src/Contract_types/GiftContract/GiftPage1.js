import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const GiftPage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      donor: {
        name: getText("donor-name"),
        address: getText("donor-address"),
        contact: getText("donor-contact"),
      },
      donee: {
        name: getText("donee-name"),
        address: getText("donee-address"),
        contact: getText("donee-contact"),
      },
      gifted_property: {
        location: getText("gift-location"),
        details: {
          building: {
            structure: getText("gift-structure"),
            usage: getText("gift-usage"),
            area: getText("gift-area"),
            current_value: getText("gift-value"),
          },
          land: {
            category: getText("land-category"),
            area: getText("land-area"),
            current_value: getText("land-value"),
          },
          others: getText("gift-others"),
        },
      },
      delivery_details: {
        delivery_date: getText("delivery-date"),
        delivery_method: getText("delivery-method"),
      },
      rights_and_obligations: {
        existing_rights: getText("existing-rights"),
        obligations: getText("obligations"),
      },
      termination_conditions: {
        reasons: getText("termination-reasons"),
        procedure: getText("termination-procedure"),
      },
      special_terms: getText("special-terms-box"),
      signature_and_seal: "서명 완료",
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

      <p className="section-title">1. 부동산의 표시</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">소재지</td>
            <td colSpan="3">{renderField("gift-location", contract.gifted_property?.location, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">건물 구조</td>
            <td>{renderField("gift-structure", contract.gifted_property?.details?.building?.structure, suggestions)}</td>
            <td className="gray">용도</td>
            <td>{renderField("gift-usage", contract.gifted_property?.details?.building?.usage, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">건물 면적</td>
            <td>{renderField("gift-area", contract.gifted_property?.details?.building?.area, suggestions)}㎡</td>
            <td className="gray">건물 가치</td>
            <td>{renderField("gift-value", contract.gifted_property?.details?.building?.current_value, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">토지 지목</td>
            <td>{renderField("land-category", contract.gifted_property?.details?.land?.category, suggestions)}</td>
            <td className="gray">토지 면적</td>
            <td>{renderField("land-area", contract.gifted_property?.details?.land?.area, suggestions)}㎡</td>
          </tr>
          <tr>
            <td className="gray">토지 가치</td>
            <td colSpan="3">{renderField("land-value", contract.gifted_property?.details?.land?.current_value, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">기타 재산</td>
            <td colSpan="3">{renderField("gift-others", contract.gifted_property?.details?.others, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 계약 내용</p>
      <p className="contract-clause">
        제1조 증여자는 수증자에게 위 부동산을 무상으로 증여하고, 수증자는 이를 승낙한다.
      </p>
      <p className="contract-clause">
        제2조 부동산의 인도일은 {renderField("delivery-date", contract.delivery_details?.delivery_date, suggestions)} 로 하며, 인도 방법은 {renderField("delivery-method", contract.delivery_details?.delivery_method, suggestions)}로 한다.
      </p>
      <p className="contract-clause">
        제3조 부동산에 관련된 권리관계는 {renderField("existing-rights", contract.rights_and_obligations?.existing_rights, suggestions)}, 의무 사항은 {renderField("obligations", contract.rights_and_obligations?.obligations, suggestions)}로 한다.
      </p>
      <p className="contract-clause">
        제4조 계약 해제 사유는 {renderField("termination-reasons", contract.termination_conditions?.reasons, suggestions)}, 절차는 {renderField("termination-procedure", contract.termination_conditions?.procedure, suggestions)}로 한다.
      </p>

      <p className="section-title">3. 특약사항</p>
      <div className="special-terms-box">
        {renderField("", contract.special_terms, suggestions)}
      </div>

      <p className="section-title">4. 계약 당사자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">증여자</td>
            <td>성명: {renderField("donor-name", contract.donor?.name, suggestions)}</td>
            <td>주소: {renderField("donor-address", contract.donor?.address, suggestions)}</td>
            <td>연락처: {renderField("donor-contact", contract.donor?.contact, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">수증자</td>
            <td>성명: {renderField("donee-name", contract.donee?.name, suggestions)}</td>
            <td>주소: {renderField("donee-address", contract.donee?.address, suggestions)}</td>
            <td>연락처: {renderField("donee-contact", contract.donee?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>
    </>
  );
});

export default GiftPage1;
