import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const LoanContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents,
  }));

  const suggestionMap = {};
  suggestions.forEach(({ field_path, suggestion_text }) => {
    const className = pathToClass(field_path);
    if (className) suggestionMap[className] = suggestion_text;
  });

  const pathToClass = (path) => ({
    "contract_type": "contract-main-title",
    "contract_date": "contract-date",
    "loan_amount.amount_korean": "loan-korean",
    "loan_amount.amount_number": "loan-number",
    "creditor.name": "creditor-name",
    "creditor.id_number": "creditor-id",
    "creditor.address": "creditor-address",
    "creditor.contact": "creditor-contact",
    "debtor.name": "debtor-name",
    "debtor.id_number": "debtor-id",
    "debtor.address": "debtor-address",
    "debtor.contact": "debtor-contact",
    "interest.rate": "interest-rate",
    "interest.payment_method": "interest-method",
    "interest.payment_date": "interest-date",
    "repayment.repayment_date": "repay-date",
    "repayment.repayment_method": "repay-method",
    "repayment.repayment_location": "repay-location",
    "repayment.account_info": "repay-account",
    "special_terms": "special-terms-box",
    "signature_and_seal": "sign-seal"
  }[path]);

  const renderField = (className, content) => {
    const suggestion = suggestionMap[className];
    const displayText = content || suggestion || "________";
    const style = content ? {} : suggestion ? { color: "#888" } : { color: "#ccc" };

    const handleInput = (e) => {
      const el = e.currentTarget;
      if (el.dataset.suggestion === "true") {
        el.innerText = "";
        el.dataset.suggestion = "false";
        el.style.color = "#000";

        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(el);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
      }
    };

    return (
      <span
        className={className}
        contentEditable
        suppressContentEditableWarning
        style={style}
        data-suggestion={content ? "false" : suggestion ? "true" : "false"}
        onInput={handleInput}
      >
        {displayText}
      </span>
    );
  };

  const extractEditedContents = () => {
    const getText = (cls) => {
      const clean = cls.replace(/^\./, "");
      const el = document.querySelector(`.${clean}`);
      if (!el || el.dataset.suggestion === "true") return "";
      return el.innerText || "";
    };

    return {
      contract_type: getText(".contract-main-title"),
      contract_date: getText(".contract-date"),
      loan_amount: {
        amount_korean: getText(".loan-korean"),
        amount_number: getText(".loan-number"),
      },
      creditor: {
        name: getText(".creditor-name"),
        id_number: getText(".creditor-id"),
        address: getText(".creditor-address"),
        contact: getText(".creditor-contact"),
      },
      debtor: {
        name: getText(".debtor-name"),
        id_number: getText(".debtor-id"),
        address: getText(".debtor-address"),
        contact: getText(".debtor-contact"),
      },
      interest: {
        rate: getText(".interest-rate"),
        payment_method: getText(".interest-method"),
        payment_date: getText(".interest-date"),
      },
      repayment: {
        repayment_date: getText(".repay-date"),
        repayment_method: getText(".repay-method"),
        repayment_location: getText(".repay-location"),
        account_info: getText(".repay-account"),
      },
      special_terms: getText(".special-terms-box"),
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 금액 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">금액(한글)</td>
            <td>{renderField("loan-korean", contract.loan_amount?.amount_korean)}</td>
            <td className="gray">금액(숫자)</td>
            <td>{renderField("loan-number", contract.loan_amount?.amount_number)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 채권자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("creditor-name", contract.creditor?.name)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("creditor-id", contract.creditor?.id_number)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("creditor-address", contract.creditor?.address)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("creditor-contact", contract.creditor?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 채무자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("debtor-name", contract.debtor?.name)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("debtor-id", contract.debtor?.id_number)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("debtor-address", contract.debtor?.address)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("debtor-contact", contract.debtor?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 이자 조건</p>
      <p className="contract-clause">
        이자율은 {renderField("interest-rate", contract.interest?.rate)}이며,
        지급 방식은 {renderField("interest-method", contract.interest?.payment_method)},
        지급일은 {renderField("interest-date", contract.interest?.payment_date)}로 한다.
      </p>

      <p className="section-title">5. 원금 상환 조건</p>
      <p className="contract-clause">
        상환일은 {renderField("repay-date", contract.repayment?.repayment_date)},
        상환 방식은 {renderField("repay-method", contract.repayment?.repayment_method)},
        상환 장소는 {renderField("repay-location", contract.repayment?.repayment_location)},
        계좌 정보는 {renderField("repay-account", contract.repayment?.account_info)}로 한다.
      </p>

      <p className="section-title">6. 특약사항</p>
      <div className="special-terms-box">{renderField("special-terms-box", contract.special_terms)}</div>
    </div>
  );
});

export default LoanContract;
