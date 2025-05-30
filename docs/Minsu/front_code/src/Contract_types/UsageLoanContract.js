import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const UsageLoanContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents,
  }));


  const pathToClass = (path) => ({
    "contract_type": "contract-main-title",
    "contract_date": "contract-date",
    "lender.name": "lender-name",
    "lender.address": "lender-address",
    "borrower.name": "borrower-name",
    "borrower.address": "borrower-address",
    "subject_property.name": "property-name",
    "loan_period.start_date": "loan-start",
    "loan_period.end_date": "loan-end",
    "purpose_of_use": "purpose-use",
    "compensation_for_damage": "compensation-damage",
    "restoration_obligation": "restoration-obligation",
    "signature_and_seal": "sign-seal"
  }[path]);

  const suggestionMap = {};
  suggestions.forEach(({ field_path, suggestion_text }) => {
    const className = pathToClass(field_path);
    if (className) suggestionMap[className] = suggestion_text;
  });

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
      lender: {
        name: getText(".lender-name"),
        address: getText(".lender-address"),
      },
      borrower: {
        name: getText(".borrower-name"),
        address: getText(".borrower-address"),
      },
      subject_property: {
        name: getText(".property-name"),
      },
      loan_period: {
        start_date: getText(".loan-start"),
        end_date: getText(".loan-end"),
      },
      purpose_of_use: getText(".purpose-use"),
      compensation_for_damage: getText(".compensation-damage"),
      restoration_obligation: getText(".restoration-obligation"),
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 대주 및 차주</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">대주 성명</td>
            <td>{renderField("lender-name", contract.lender?.name)}</td>
            <td className="gray">주소</td>
            <td>{renderField("lender-address", contract.lender?.address)}</td>
          </tr>
          <tr>
            <td className="gray">차주 성명</td>
            <td>{renderField("borrower-name", contract.borrower?.name)}</td>
            <td className="gray">주소</td>
            <td>{renderField("borrower-address", contract.borrower?.address)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 목적물 및 용도</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">목적물</td>
            <td>{renderField("property-name", contract.subject_property?.name)}</td>
            <td className="gray">용도</td>
            <td>{renderField("purpose-use", contract.purpose_of_use)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 사용대차 기간</p>
      <p className="contract-clause">
        사용 기간은 {renderField("loan-start", contract.loan_period?.start_date)}부터 {renderField("loan-end", contract.loan_period?.end_date)}까지로 한다.
      </p>

      <p className="section-title">4. 손해배상 및 계약 위반</p>
      <p className="contract-clause">
        목적물의 손해나 계약 위반 시 {renderField("compensation-damage", contract.compensation_for_damage)} 책임을 진다.
      </p>

      <p className="section-title">5. 원상회복</p>
      <p className="contract-clause">
        계약 종료 시 목적물은 {renderField("restoration-obligation", contract.restoration_obligation)} 상태로 원상회복한다.
      </p>
    </div>
  );
});

export default UsageLoanContract;
