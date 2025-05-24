import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const GiftContract = forwardRef(({ contract }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents
  }));

  const extractEditedContents = () => {
    const getText = (selector) => document.querySelector(selector)?.innerText || "";

    return {
      contract_type: getText(".contract-main-title"),
      contract_date: getText(".contract-date"),
      donor: {
        name: getText(".donor-name"),
        address: getText(".donor-address"),
        contact: getText(".donor-contact")
      },
      donee: {
        name: getText(".donee-name"),
        address: getText(".donee-address"),
        contact: getText(".donee-contact")
      },
      gifted_property: {
        location: getText(".gift-location"),
        details: {
          building: {
            structure: getText(".gift-structure"),
            usage: getText(".gift-usage"),
            area: getText(".gift-area"),
            current_value: getText(".gift-value")
          },
          land: {
            category: getText(".land-category"),
            area: getText(".land-area"),
            current_value: getText(".land-value")
          },
          others: getText(".gift-others")
        }
      },
      delivery_details: {
        delivery_date: getText(".delivery-date"),
        delivery_method: getText(".delivery-method")
      },
      rights_and_obligations: {
        existing_rights: getText(".existing-rights"),
        obligations: getText(".obligations")
      },
      termination_conditions: {
        reasons: getText(".termination-reasons"),
        procedure: getText(".termination-procedure")
      },
      special_terms: getText(".special-terms-box"),
      signature_and_seal: "서명 완료"
    };
  };

  const renderField = (className, content) => (
    <span className={className} contentEditable suppressContentEditableWarning>
      {content || "________"}
    </span>
  );

  return (
    <div className="gift-contract">
      <div>
        <h1 className="contract-main-title" contentEditable suppressContentEditableWarning>
          {contract.contract_type}
        </h1>

        <p className="section-title">1. 부동산의 표시</p>
        <table className="contract-table">
          <tbody>
            <tr>
              <td className="gray">소재지</td>
              <td colSpan="3">{renderField("gift-location", contract.gifted_property?.location)}</td>
            </tr>
            <tr>
              <td className="gray">건물 구조</td>
              <td>{renderField("gift-structure", contract.gifted_property?.details?.building?.structure)}</td>
              <td className="gray">용도</td>
              <td>{renderField("gift-usage", contract.gifted_property?.details?.building?.usage)}</td>
            </tr>
            <tr>
              <td className="gray">건물 면적</td>
              <td>{renderField("gift-area", contract.gifted_property?.details?.building?.area)}㎡</td>
              <td className="gray">건물 가치</td>
              <td>{renderField("gift-value", contract.gifted_property?.details?.building?.current_value)}</td>
            </tr>
            <tr>
              <td className="gray">토지 지목</td>
              <td>{renderField("land-category", contract.gifted_property?.details?.land?.category)}</td>
              <td className="gray">토지 면적</td>
              <td>{renderField("land-area", contract.gifted_property?.details?.land?.area)}㎡</td>
            </tr>
            <tr>
              <td className="gray">토지 가치</td>
              <td colSpan="3">{renderField("land-value", contract.gifted_property?.details?.land?.current_value)}</td>
            </tr>
            <tr>
              <td className="gray">기타 재산</td>
              <td colSpan="3">{renderField("gift-others", contract.gifted_property?.details?.others)}</td>
            </tr>
          </tbody>
        </table>

        <p className="section-title">2. 계약 내용</p>
        <p className="contract-clause">
          제1조 증여자는 수증자에게 위 부동산을 무상으로 증여하고, 수증자는 이를 승낙한다.
        </p>
        <p className="contract-clause">
          제2조 부동산의 인도일은 {renderField("delivery-date", contract.delivery_details?.delivery_date)} 로 하며, 인도 방법은 {renderField("delivery-method", contract.delivery_details?.delivery_method)}로 한다.
        </p>
        <p className="contract-clause">
          제3조 부동산에 관련된 권리관계는 {renderField("existing-rights", contract.rights_and_obligations?.existing_rights)}, 의무 사항은 {renderField("obligations", contract.rights_and_obligations?.obligations)}로 한다.
        </p>
        <p className="contract-clause">
          제4조 계약 해제 사유는 {renderField("termination-reasons", contract.termination_conditions?.reasons)}, 절차는 {renderField("termination-procedure", contract.termination_conditions?.procedure)}로 한다.
        </p>

        <p className="section-title">3. 특약사항</p>
        <div className="special-terms-box">
          {renderField("", contract.special_terms)}
        </div>

        <p className="contract-date">
          {renderField("contract-date", contract.contract_date || "20    년    월    일")}
        </p>

        <p className="section-title">4. 계약 당사자</p>
        <table className="contract-table">
          <tbody>
            <tr>
              <td className="gray">증여자</td>
              <td>성명: {renderField("donor-name", contract.donor?.name)}</td>
              <td>주소: {renderField("donor-address", contract.donor?.address)}</td>
              <td>연락처: {renderField("donor-contact", contract.donor?.contact)}</td>
            </tr>
            <tr>
              <td className="gray">수증자</td>
              <td>성명: {renderField("donee-name", contract.donee?.name)}</td>
              <td>주소: {renderField("donee-address", contract.donee?.address)}</td>
              <td>연락처: {renderField("donee-contact", contract.donee?.contact)}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
});

export default GiftContract;
