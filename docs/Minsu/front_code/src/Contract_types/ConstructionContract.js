// src/Contract_types/ConstructionContract.js

import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const ConstructionContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({ extract: extractEditedContents }));

  const pathToClass = (path) => ({
    "contract_type":                         "contract-main-title",
    "contract_date":                         "contract-date",
    "contractee.name":                       "contractee-name",
    "contractee.business_number":            "contractee-bn",
    "contractee.address":                    "contractee-address",
    "contractee.contact":                    "contractee-contact",
    "contractor.name":                       "contractor-name",
    "contractor.business_number":            "contractor-bn",
    "contractor.address":                    "contractor-address",
    "contractor.contact":                    "contractor-contact",
    "contract_details.construction_name":    "construction-name",
    "contract_details.construction_location":"construction-location",
    "contract_details.construction_period.start_date": "construction-start",
    "contract_details.construction_period.end_date":   "construction-end",
    "contract_details.construction_scope":   "construction-scope",
    "contract_details.design_document_reference":"design-doc",
    "contract_amount.total_amount":          "amount-total",
    "contract_amount.vat_included":          "amount-vat",
    "contract_amount.payment_method":        "amount-method",
    "contract_amount.payment_schedule":      "amount-schedule",
    "obligation_and_rights.ordering_party_obligation":"obligation-order",
    "obligation_and_rights.contractor_obligation":"obligation-contractor",
    "delay_penalty":                         "delay-penalty",
    "warranty_period":                       "warranty-period",
    "dispute_resolution":                    "dispute-resolution",
    "special_terms":                         "special-terms-box",
    "signature_and_seal":                    "sign-seal"
  }[path]);

  const suggestionMap = {};
  suggestions.forEach(({ field_path, suggestion_text }) => {
    const cls = pathToClass(field_path);
    if (cls) suggestionMap[cls] = suggestion_text;
  });

  const renderField = (className, content) => {
    const suggestion = suggestionMap[className];
    const isSug = !content && !!suggestion;
    const display = content || suggestion || "________";
    const style = content ? {} : isSug ? { color: "#888" } : { color: "#ccc" };

    const onInput = (e) => {
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
        data-suggestion={isSug ? "true" : "false"}
        onInput={onInput}
      >
        {display}
      </span>
    );
  };

  const extractEditedContents = () => {
    const getText = (cls) => {
      const el = document.querySelector(`.${cls.replace(/^\./, "")}`);
      if (!el || el.dataset.suggestion === "true") return "";
      return el.innerText.trim();
    };

    return {
      contract_type: getText(".contract-main-title"),
      contract_date: getText(".contract-date"),
      contractee: {
        name:            getText(".contractee-name"),
        business_number: getText(".contractee-bn"),
        address:         getText(".contractee-address"),
        contact:         getText(".contractee-contact")
      },
      contractor: {
        name:            getText(".contractor-name"),
        business_number: getText(".contractor-bn"),
        address:         getText(".contractor-address"),
        contact:         getText(".contractor-contact")
      },
      contract_details: {
        construction_name:        getText(".construction-name"),
        construction_location:    getText(".construction-location"),
        construction_period: {
          start_date: getText(".construction-start"),
          end_date:   getText(".construction-end")
        },
        construction_scope:       getText(".construction-scope"),
        design_document_reference:getText(".design-doc")
      },
      contract_amount: {
        total_amount:     getText(".amount-total"),
        vat_included:     getText(".amount-vat") === "포함",
        payment_method:   getText(".amount-method"),
        payment_schedule: getText(".amount-schedule")
      },
      obligation_and_rights: {
        ordering_party_obligation: getText(".obligation-order"),
        contractor_obligation:     getText(".obligation-contractor")
      },
      delay_penalty:      getText(".delay-penalty"),
      warranty_period:    getText(".warranty-period"),
      dispute_resolution: getText(".dispute-resolution"),
      special_terms:      getText(".special-terms-box"),
      signature_and_seal: getText(".sign-seal")
    };
  };

  return (
    <div className="gift-contract">
      <div className="section" id="section-0">
        <h1 className="contract-main-title">
          {renderField("contract-main-title", contract.contract_type)}
        </h1>
        <p className="contract-date">
          {renderField("contract-date", contract.contract_date)}
        </p>
      </div>

      <div className="section" id="section-1">
        <p className="section-title">1. 도급인 및 수급인</p>
        <table className="contract-table">
          <tbody>
            <tr>
              <td className="gray">도급인</td>
              <td>{renderField("contractee-name", contract.contractee?.name)}</td>
              <td>{renderField("contractee-bn", contract.contractee?.business_number)}</td>
              <td>{renderField("contractee-address", contract.contractee?.address)}</td>
              <td>{renderField("contractee-contact", contract.contractee?.contact)}</td>
            </tr>
            <tr>
              <td className="gray">수급인</td>
              <td>{renderField("contractor-name", contract.contractor?.name)}</td>
              <td>{renderField("contractor-bn", contract.contractor?.business_number)}</td>
              <td>{renderField("contractor-address", contract.contractor?.address)}</td>
              <td>{renderField("contractor-contact", contract.contractor?.contact)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section" id="section-2">
        <p className="section-title">2. 공사 정보</p>
        <table className="contract-table">
          <tbody>
            <tr>
              <td className="gray">공사명</td>
              <td>{renderField("construction-name", contract.contract_details?.construction_name)}</td>
            </tr>
            <tr>
              <td className="gray">공사 위치</td>
              <td>{renderField("construction-location", contract.contract_details?.construction_location)}</td>
            </tr>
            <tr>
              <td className="gray">공사 기간</td>
              <td>
                {renderField("construction-start", contract.contract_details?.construction_period?.start_date)} ~{' '}
                {renderField("construction-end", contract.contract_details?.construction_period?.end_date)}
              </td>
            </tr>
            <tr>
              <td className="gray">공사 범위</td>
              <td>{renderField("construction-scope", contract.contract_details?.construction_scope)}</td>
            </tr>
            <tr>
              <td className="gray">설계 도서</td>
              <td>{renderField("design-doc", contract.contract_details?.design_document_reference)}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="section" id="section-3">
        <p className="section-title">3. 도급금액</p>
        <p className="contract-clause">
          총액: {renderField("amount-total", contract.contract_amount?.total_amount)} (부가세: {renderField("amount-vat", contract.contract_amount?.vat_included ? "포함" : "별도")})
        </p>
        <p className="contract-clause">
          지급 방법: {renderField("amount-method", contract.contract_amount?.payment_method)}
        </p>
        <p className="contract-clause">
          지급 일정: {renderField("amount-schedule", contract.contract_amount?.payment_schedule)}
        </p>
      </div>

      <div className="section" id="section-4">
        <p className="section-title">4. 의무사항</p>
        <p className="contract-clause">
          도급인 의무: {renderField("obligation-order", contract.obligation_and_rights?.ordering_party_obligation)}
        </p>
        <p className="contract-clause">
          수급인 의무: {renderField("obligation-contractor", contract.obligation_and_rights?.contractor_obligation)}
        </p>
      </div>

      <div className="section" id="section-5">
        <p className="section-title">5. 지연손해금</p>
        <p className="contract-clause">{renderField("delay-penalty", contract.delay_penalty)}</p>
      </div>

      <div className="section" id="section-6">
        <p className="section-title">6. 하자담보 기간</p>
        <p className="contract-clause">{renderField("warranty-period", contract.warranty_period)}</p>
      </div>

      {/* 7. 분쟁 해결 */}
      <div className="section" id="section-7">
        <p className="section-title">7. 분쟁 해결</p>
        <p className="contract-clause">{renderField("dispute-resolution", contract.dispute_resolution)}</p>
      </div>

      {/* 8. 특약사항 */}
      <div className="section" id="section-8">
        <p className="section-title">8. 특약사항</p>
        <div className="special-terms-box">
          {renderField("special-terms-box", contract.special_terms)}
        </div>
      </div>
    </div>
  );
});

export default ConstructionContract;
