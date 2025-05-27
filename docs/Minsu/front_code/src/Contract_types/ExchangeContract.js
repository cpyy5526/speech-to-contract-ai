import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const ExchangeContract = forwardRef(({ contract, suggestions = [] }, ref) => {
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
    "property_A.location": "propertyA-location",
    "property_A.land_category": "propertyA-category",
    "property_A.land_area": "propertyA-area",
    "property_A.building_details": "propertyA-building",
    "property_B.location": "propertyB-location",
    "property_B.land_category": "propertyB-category",
    "property_B.land_area": "propertyB-area",
    "property_B.building_details": "propertyB-building",
    "party_A.name": "partyA-name",
    "party_A.id_number": "partyA-id",
    "party_A.address": "partyA-address",
    "party_A.contact": "partyA-contact",
    "party_B.name": "partyB-name",
    "party_B.id_number": "partyB-id",
    "party_B.address": "partyB-address",
    "party_B.contact": "partyB-contact",
    "exchange_payment.total_price": "exchange-total",
    "exchange_payment.down_payment.amount": "exchange-down",
    "exchange_payment.down_payment.payment_date": "date-down",
    "exchange_payment.interim_payment.amount": "exchange-interim",
    "exchange_payment.interim_payment.payment_date": "date-interim",
    "exchange_payment.balance_payment.amount": "exchange-balance",
    "exchange_payment.balance_payment.payment_date": "date-balance",
    "ownership_transfer.document_transfer_date": "date-doc",
    "ownership_transfer.property_delivery_date": "date-delivery",
    "termination.penalty_amount": "penalty",
    "broker.office_name": "broker-office",
    "broker.office_address": "broker-address",
    "broker.representative": "broker-representative",
    "broker.registration_number": "broker-regnum",
    "broker.broker_name": "broker-name",
    "special_terms": "special-terms-box",
    "signature_and_seal": "sign-seal",
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
      property_A: {
        location: getText(".propertyA-location"),
        land_category: getText(".propertyA-category"),
        land_area: getText(".propertyA-area"),
        building_details: getText(".propertyA-building"),
      },
      property_B: {
        location: getText(".propertyB-location"),
        land_category: getText(".propertyB-category"),
        land_area: getText(".propertyB-area"),
        building_details: getText(".propertyB-building"),
      },
      party_A: {
        name: getText(".partyA-name"),
        id_number: getText(".partyA-id"),
        address: getText(".partyA-address"),
        contact: getText(".partyA-contact"),
      },
      party_B: {
        name: getText(".partyB-name"),
        id_number: getText(".partyB-id"),
        address: getText(".partyB-address"),
        contact: getText(".partyB-contact"),
      },
      exchange_payment: {
        total_price: getText(".exchange-total"),
        down_payment: {
          amount: getText(".exchange-down"),
          payment_date: getText(".date-down"),
        },
        interim_payment: {
          amount: getText(".exchange-interim"),
          payment_date: getText(".date-interim"),
        },
        balance_payment: {
          amount: getText(".exchange-balance"),
          payment_date: getText(".date-balance"),
        },
      },
      ownership_transfer: {
        document_transfer_date: getText(".date-doc"),
        property_delivery_date: getText(".date-delivery"),
      },
      termination: {
        penalty_amount: getText(".penalty"),
      },
      broker: {
        office_name: getText(".broker-office"),
        office_address: getText(".broker-address"),
        representative: getText(".broker-representative"),
        registration_number: getText(".broker-regnum"),
        broker_name: getText(".broker-name"),
      },
      special_terms: getText(".special-terms-box"),
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 부동산 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">갑 부동산 위치</td>
            <td>{renderField("propertyA-location", contract.property_A?.location)}</td>
            <td className="gray">지목</td>
            <td>{renderField("propertyA-category", contract.property_A?.land_category)}</td>
          </tr>
          <tr>
            <td className="gray">면적</td>
            <td>{renderField("propertyA-area", contract.property_A?.land_area)}</td>
            <td className="gray">건물 정보</td>
            <td>{renderField("propertyA-building", contract.property_A?.building_details)}</td>
          </tr>
          <tr>
            <td className="gray">을 부동산 위치</td>
            <td>{renderField("propertyB-location", contract.property_B?.location)}</td>
            <td className="gray">지목</td>
            <td>{renderField("propertyB-category", contract.property_B?.land_category)}</td>
          </tr>
          <tr>
            <td className="gray">면적</td>
            <td>{renderField("propertyB-area", contract.property_B?.land_area)}</td>
            <td className="gray">건물 정보</td>
            <td>{renderField("propertyB-building", contract.property_B?.building_details)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 당사자 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">갑</td>
            <td>{renderField("partyA-name", contract.party_A?.name)}</td>
            <td>{renderField("partyA-id", contract.party_A?.id_number)}</td>
            <td>{renderField("partyA-address", contract.party_A?.address)}</td>
            <td>{renderField("partyA-contact", contract.party_A?.contact)}</td>
          </tr>
          <tr>
            <td className="gray">을</td>
            <td>{renderField("partyB-name", contract.party_B?.name)}</td>
            <td>{renderField("partyB-id", contract.party_B?.id_number)}</td>
            <td>{renderField("partyB-address", contract.party_B?.address)}</td>
            <td>{renderField("partyB-contact", contract.party_B?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 교환 차액 지급</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">총액</td>
            <td>{renderField("exchange-total", contract.exchange_payment?.total_price)}</td>
            <td className="gray">계약금</td>
            <td>{renderField("exchange-down", contract.exchange_payment?.down_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-down", contract.exchange_payment?.down_payment?.payment_date)}</td>
          </tr>
          <tr>
            <td className="gray">중도금</td>
            <td>{renderField("exchange-interim", contract.exchange_payment?.interim_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-interim", contract.exchange_payment?.interim_payment?.payment_date)}</td>
            <td className="gray">잔금</td>
            <td>{renderField("exchange-balance", contract.exchange_payment?.balance_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-balance", contract.exchange_payment?.balance_payment?.payment_date)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 소유권 이전</p>
      <p className="contract-clause">
        서류 이전일은 {renderField("date-doc", contract.ownership_transfer?.document_transfer_date)},
        부동산 인도일은 {renderField("date-delivery", contract.ownership_transfer?.property_delivery_date)}로 한다.
      </p>

      <p className="section-title">5. 계약 해제 및 위약금</p>
      <p className="contract-clause">
        계약 해제 시 위약금은 {renderField("penalty", contract.termination?.penalty_amount)} 원으로 한다.
      </p>

      <p className="section-title">6. 중개사 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">중개사무소 명칭</td>
            <td>{renderField("broker-office", contract.broker?.office_name)}</td>
            <td className="gray">주소</td>
            <td>{renderField("broker-address", contract.broker?.office_address)}</td>
          </tr>
          <tr>
            <td className="gray">대표자</td>
            <td>{renderField("broker-representative", contract.broker?.representative)}</td>
            <td className="gray">등록번호</td>
            <td>{renderField("broker-regnum", contract.broker?.registration_number)}</td>
            <td className="gray">담당 중개사</td>
            <td>{renderField("broker-name", contract.broker?.broker_name)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">7. 특약사항</p>
      <div className="special-terms-box">{renderField("special-terms-box", contract.special_terms)}</div>
    </div>
  );
});

export default ExchangeContract;