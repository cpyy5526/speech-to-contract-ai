import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const LeaseContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents,
  }));

  const pathToClass = (path) => ({
    "contract_type": "contract-main-title",
    "contract_date": "contract-date",
    "property.address": "property-address",
    "property.land_category": "property-category",
    "property.area": "property-area",
    "property.building_details": "property-building",
    "lessor.name": "lessor-name",
    "lessor.resident_number": "lessor-id",
    "lessor.address": "lessor-address",
    "lessor.contact": "lessor-contact",
    "lessee.name": "lessee-name",
    "lessee.resident_number": "lessee-id",
    "lessee.address": "lessee-address",
    "lessee.contact": "lessee-contact",
    "lease_terms.deposit": "lease-deposit",
    "lease_terms.monthly_rent": "lease-rent",
    "lease_terms.contract_period.start_date": "lease-start",
    "lease_terms.contract_period.end_date": "lease-end",
    "lease_terms.payment_date": "lease-payment",
    "management_fee": "management-fee",
    "use_purpose": "use-purpose",
    "delivery_date": "delivery-date",
    "termination": "termination",
    "special_terms": "special-terms-box",
    "real_estate_agent.office_address": "agent-address",
    "real_estate_agent.office_name": "agent-office",
    "real_estate_agent.representative_name": "agent-rep",
    "real_estate_agent.registration_number": "agent-regnum",
    "real_estate_agent.broker_name": "agent-broker",
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
      property: {
        address: getText(".property-address"),
        land_category: getText(".property-category"),
        area: getText(".property-area"),
        building_details: getText(".property-building"),
      },
      lessor: {
        name: getText(".lessor-name"),
        resident_number: getText(".lessor-id"),
        address: getText(".lessor-address"),
        contact: getText(".lessor-contact"),
      },
      lessee: {
        name: getText(".lessee-name"),
        resident_number: getText(".lessee-id"),
        address: getText(".lessee-address"),
        contact: getText(".lessee-contact"),
      },
      lease_terms: {
        deposit: getText(".lease-deposit"),
        monthly_rent: getText(".lease-rent"),
        contract_period: {
          start_date: getText(".lease-start"),
          end_date: getText(".lease-end"),
        },
        payment_date: getText(".lease-payment"),
      },
      management_fee: getText(".management-fee"),
      use_purpose: getText(".use-purpose"),
      delivery_date: getText(".delivery-date"),
      termination: getText(".termination"),
      special_terms: getText(".special-terms-box"),
      real_estate_agent: {
        office_address: getText(".agent-address"),
        office_name: getText(".agent-office"),
        representative_name: getText(".agent-rep"),
        registration_number: getText(".agent-regnum"),
        broker_name: getText(".agent-broker"),
      },
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 임대차 목적물</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">주소</td>
            <td>{renderField("property-address", contract.property?.address)}</td>
            <td className="gray">지목</td>
            <td>{renderField("property-category", contract.property?.land_category)}</td>
          </tr>
          <tr>
            <td className="gray">면적</td>
            <td>{renderField("property-area", contract.property?.area)}㎡</td>
            <td className="gray">건물 내역</td>
            <td>{renderField("property-building", contract.property?.building_details)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 임대인 및 임차인 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">임대인</td>
            <td>{renderField("lessor-name", contract.lessor?.name)}</td>
            <td>{renderField("lessor-id", contract.lessor?.resident_number)}</td>
            <td>{renderField("lessor-address", contract.lessor?.address)}</td>
            <td>{renderField("lessor-contact", contract.lessor?.contact)}</td>
          </tr>
          <tr>
            <td className="gray">임차인</td>
            <td>{renderField("lessee-name", contract.lessee?.name)}</td>
            <td>{renderField("lessee-id", contract.lessee?.resident_number)}</td>
            <td>{renderField("lessee-address", contract.lessee?.address)}</td>
            <td>{renderField("lessee-contact", contract.lessee?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 임대차 조건</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">보증금</td>
            <td>{renderField("lease-deposit", contract.lease_terms?.deposit)}</td>
            <td className="gray">월세</td>
            <td>{renderField("lease-rent", contract.lease_terms?.monthly_rent)}</td>
          </tr>
          <tr>
            <td className="gray">계약기간</td>
            <td>{renderField("lease-start", contract.lease_terms?.contract_period?.start_date)} ~ {renderField("lease-end", contract.lease_terms?.contract_period?.end_date)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("lease-payment", contract.lease_terms?.payment_date)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 기타 조건</p>
      <p className="contract-clause">관리비: {renderField("management-fee", contract.management_fee)}</p>
      <p className="contract-clause">용도: {renderField("use-purpose", contract.use_purpose)}</p>
      <p className="contract-clause">인도일: {renderField("delivery-date", contract.delivery_date)}</p>
      <p className="contract-clause">계약 해지 조건: {renderField("termination", contract.termination)}</p>

      <p className="section-title">5. 특약사항</p>
      <div className="special-terms-box">{renderField("special-terms-box", contract.special_terms)}</div>

      <p className="section-title">6. 중개업소 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">사무소명</td>
            <td>{renderField("agent-office", contract.real_estate_agent?.office_name)}</td>
            <td className="gray">대표자</td>
            <td>{renderField("agent-rep", contract.real_estate_agent?.representative_name)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td>{renderField("agent-address", contract.real_estate_agent?.office_address)}</td>
            <td className="gray">등록번호</td>
            <td>{renderField("agent-regnum", contract.real_estate_agent?.registration_number)}</td>
          </tr>
          <tr>
            <td className="gray">공인중개사</td>
            <td colSpan="3">{renderField("agent-broker", contract.real_estate_agent?.broker_name)}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
});

export default LeaseContract;
