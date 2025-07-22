import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const UsageLoanPage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      lender: {
        name: getText("lender-name"),
        address: getText("lender-address"),
      },
      borrower: {
        name: getText("borrower-name"),
        address: getText("borrower-address"),
      },
      subject_property: {
        name: getText("property-name"),
      },
      loan_period: {
        start_date: getText("loan-start"),
        end_date: getText("loan-end"),
      },
      purpose_of_use: getText("purpose-use"),
      compensation_for_damage: getText("compensation-damage"),
      restoration_obligation: getText("restoration-obligation"),
      signature_and_seal: getText("sign-seal"),
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText || "";
  };

  return (
    <>
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type, suggestions)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date, suggestions)}</p>

      <p className="section-title">1. 대주 및 차주</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">대주 성명</td>
            <td>{renderField("lender-name", contract.lender?.name, suggestions)}</td>
            <td className="gray">주소</td>
            <td>{renderField("lender-address", contract.lender?.address, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">차주 성명</td>
            <td>{renderField("borrower-name", contract.borrower?.name, suggestions)}</td>
            <td className="gray">주소</td>
            <td>{renderField("borrower-address", contract.borrower?.address, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 목적물</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">목적물 명칭</td>
            <td>{renderField("property-name", contract.subject_property?.name, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 사용대차 기간</p>
      <p className="contract-clause">
        사용 기간은 {renderField("loan-start", contract.loan_period?.start_date, suggestions)}부터 {renderField("loan-end", contract.loan_period?.end_date, suggestions)}까지로 한다.
      </p>

      <p className="section-title">4. 용도 및 책임</p>
      <p className="contract-clause">
        목적물의 용도는 {renderField("purpose-use", contract.purpose_of_use, suggestions)}로 하며, 손해 발생 시 {renderField("compensation-damage", contract.compensation_for_damage, suggestions)} 책임을 진다.
      </p>

      <p className="section-title">5. 원상회복</p>
      <p className="contract-clause">
        계약 종료 시 목적물은 {renderField("restoration-obligation", contract.restoration_obligation, suggestions)} 상태로 원상회복하여야 한다.
      </p>

      <p className="section-title">6. 서명란</p>
      <p className="signature-block">
        본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
      </p>

      <table className="contract-table" style={{ marginTop: "20px" }}>
        <tbody>
          <tr>
            <td className="gray">대주</td>
            <td>{renderField("lender-sign", contract.lender?.name, suggestions)} (인)</td>
          </tr>
          <tr>
            <td className="gray">차주</td>
            <td>{renderField("borrower-sign", contract.borrower?.name, suggestions)} (인)</td>
          </tr>
        </tbody>
      </table>

    </>
  );
});

export default UsageLoanPage1;
