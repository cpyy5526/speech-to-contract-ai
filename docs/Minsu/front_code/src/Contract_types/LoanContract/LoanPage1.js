import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const LoanPage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      loan_amount: {
        amount_korean: getText("loan-korean"),
        amount_number: getText("loan-number"),
      },
      creditor: {
        name: getText("creditor-name"),
        id_number: getText("creditor-id"),
        address: getText("creditor-address"),
        contact: getText("creditor-contact"),
      },
      debtor: {
        name: getText("debtor-name"),
        id_number: getText("debtor-id"),
        address: getText("debtor-address"),
        contact: getText("debtor-contact"),
      },
      interest: {
        rate: getText("interest-rate"),
        payment_method: getText("interest-method"),
        payment_date: getText("interest-date"),
      },
      repayment: {
        repayment_date: getText("repay-date"),
        repayment_method: getText("repay-method"),
        repayment_location: getText("repay-location"),
        account_info: getText("repay-account"),
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

      <p className="section-title">1. 금액 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">금액(한글)</td>
            <td>{renderField("loan-korean", contract.loan_amount?.amount_korean, suggestions)}</td>
            <td className="gray">금액(숫자)</td>
            <td>{renderField("loan-number", contract.loan_amount?.amount_number, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 채권자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("creditor-name", contract.creditor?.name, suggestions)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("creditor-id", contract.creditor?.id_number, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("creditor-address", contract.creditor?.address, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("creditor-contact", contract.creditor?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 채무자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("debtor-name", contract.debtor?.name, suggestions)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("debtor-id", contract.debtor?.id_number, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("debtor-address", contract.debtor?.address, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("debtor-contact", contract.debtor?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 이자 조건</p>
      <p className="contract-clause">
        이자율은 {renderField("interest-rate", contract.interest?.rate, suggestions)}이며, 지급 방식은{" "}
        {renderField("interest-method", contract.interest?.payment_method, suggestions)}, 지급일은{" "}
        {renderField("interest-date", contract.interest?.payment_date, suggestions)}로 한다.
      </p>

      <p className="section-title">5. 원금 상환 조건</p>
      <p className="contract-clause">
        상환일은 {renderField("repay-date", contract.repayment?.repayment_date, suggestions)}, 상환 방식은{" "}
        {renderField("repay-method", contract.repayment?.repayment_method, suggestions)}, 상환 장소는{" "}
        {renderField("repay-location", contract.repayment?.repayment_location, suggestions)}, 계좌 정보는{" "}
        {renderField("repay-account", contract.repayment?.account_info, suggestions)}로 한다.
      </p>

      <p className="section-title">6. 특약사항</p>
      <div className="special-terms-box">{renderField("special-terms-box", contract.special_terms, suggestions)}</div>

      <p className="section-title">7. 서명란</p>
      <p className="signature-block">
        본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
      </p>

      <table className="contract-table" style={{ marginTop: "20px" }}>
        <tbody>
          <tr>
            <td className="gray">채권자</td>
            <td>{renderField("creditor-sign", contract.creditor?.name, suggestions)} (인)</td>
          </tr>
          <tr>
            <td className="gray">채무자</td>
            <td>{renderField("debtor-sign", contract.debtor?.name, suggestions)} (인)</td>
          </tr>
        </tbody>
      </table>

    </>
  );
});

export default LoanPage1;
