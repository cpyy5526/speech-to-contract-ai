import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const ConstructionPage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      contractee: {
        name: getText("contractee-name"),
        business_number: getText("contractee-bn"),
        address: getText("contractee-address"),
        contact: getText("contractee-contact"),
      },
      contractor: {
        name: getText("contractor-name"),
        business_number: getText("contractor-bn"),
        address: getText("contractor-address"),
        contact: getText("contractor-contact"),
      },
      contract_details: {
        construction_name: getText("construction-name"),
        construction_location: getText("construction-location"),
        construction_period: {
          start_date: getText("construction-start"),
          end_date: getText("construction-end"),
        },
        construction_scope: getText("construction-scope"),
        design_document_reference: getText("design-doc"),
      },
      contract_amount: {
        total_amount: getText("amount-total"),
        vat_included: getText("amount-vat") === "포함",
        payment_method: getText("amount-method"),
        payment_schedule: getText("amount-schedule"),
      },
      obligation_and_rights: {
        ordering_party_obligation: getText("obligation-order"),
        contractor_obligation: getText("obligation-contractor"),
      },
      delay_penalty: getText("delay-penalty"),
      warranty_period: getText("warranty-period"),
      dispute_resolution: getText("dispute-resolution"),
      special_terms: getText("special-terms-box"),
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <div className="section">
      <h1 className="contract-main-title">
        {renderField("contract-main-title", contract.contract_type, suggestions)}
      </h1>
      <p className="contract-date">
        {renderField("contract-date", contract.contract_date, suggestions)}
      </p>

      <p className="section-title">1. 도급인 및 수급인</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">도급인</td>
            <td>{renderField("contractee-name", contract.contractee?.name, suggestions)}</td>
            <td>{renderField("contractee-bn", contract.contractee?.business_number, suggestions)}</td>
            <td>{renderField("contractee-address", contract.contractee?.address, suggestions)}</td>
            <td>{renderField("contractee-contact", contract.contractee?.contact, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">수급인</td>
            <td>{renderField("contractor-name", contract.contractor?.name, suggestions)}</td>
            <td>{renderField("contractor-bn", contract.contractor?.business_number, suggestions)}</td>
            <td>{renderField("contractor-address", contract.contractor?.address, suggestions)}</td>
            <td>{renderField("contractor-contact", contract.contractor?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 공사 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">공사명</td>
            <td>{renderField("construction-name", contract.contract_details?.construction_name, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">공사 위치</td>
            <td>{renderField("construction-location", contract.contract_details?.construction_location, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">공사 기간</td>
            <td>
              {renderField("construction-start", contract.contract_details?.construction_period?.start_date, suggestions)} ~{' '}
              {renderField("construction-end", contract.contract_details?.construction_period?.end_date, suggestions)}
            </td>
          </tr>
          <tr>
            <td className="gray">공사 범위</td>
            <td>{renderField("construction-scope", contract.contract_details?.construction_scope, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">설계 도서</td>
            <td>{renderField("design-doc", contract.contract_details?.design_document_reference, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 도급금액</p>
      <p className="contract-clause">
        총액: {renderField("amount-total", contract.contract_amount?.total_amount, suggestions)} (부가세: {renderField("amount-vat", contract.contract_amount?.vat_included ? "포함" : "별도", suggestions)})
      </p>
      <p className="contract-clause">
        지급 방법: {renderField("amount-method", contract.contract_amount?.payment_method, suggestions)}
      </p>
      <p className="contract-clause">
        지급 일정: {renderField("amount-schedule", contract.contract_amount?.payment_schedule, suggestions)}
      </p>

      <p className="section-title">4. 의무사항</p>
      <p className="contract-clause">
        도급인 의무: {renderField("obligation-order", contract.obligation_and_rights?.ordering_party_obligation, suggestions)}
      </p>
      <p className="contract-clause">
        수급인 의무: {renderField("obligation-contractor", contract.obligation_and_rights?.contractor_obligation, suggestions)}
      </p>

      <p className="section-title">5. 지연손해금</p>
      <p className="contract-clause">{renderField("delay-penalty", contract.delay_penalty, suggestions)}</p>

      <p className="section-title">6. 하자담보 기간</p>
      <p className="contract-clause">{renderField("warranty-period", contract.warranty_period, suggestions)}</p>

      <p className="section-title">7. 분쟁 해결</p>
      <p className="contract-clause">{renderField("dispute-resolution", contract.dispute_resolution, suggestions)}</p>

      <p className="section-title">8. 특약사항</p>
      <div className="special-terms-box">
        {renderField("special-terms-box", contract.special_terms, suggestions)}
      </div>
    </div>
  );
});

export default ConstructionPage1;
