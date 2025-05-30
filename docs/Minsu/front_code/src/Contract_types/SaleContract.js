// Contract_types/SaleContract.js
import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css"; // ✅ 동일 CSS 사용

const SaleContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents,
  }));

  const pathToClass = (path) => ({
    "contract_type": "contract-main-title",
    "contract_date": "contract-date",
    "seller.name": "seller-name",
    "seller.id_number": "seller-id",
    "seller.address": "seller-address",
    "seller.contact": "seller-contact",
    "buyer.name": "buyer-name",
    "buyer.id_number": "buyer-id",
    "buyer.address": "buyer-address",
    "buyer.contact": "buyer-contact",
    "property.location": "property-location",
    "property.land_category": "property-category",
    "property.land_area": "property-area",
    "property.building_details": "property-building",
    "sale_price.total_price": "price-total",
    "sale_price.down_payment.amount": "price-down",
    "sale_price.down_payment.payment_date": "date-down",
    "sale_price.interim_payment.amount": "price-interim",
    "sale_price.interim_payment.payment_date": "date-interim",
    "sale_price.balance_payment.amount": "price-balance",
    "sale_price.balance_payment.payment_date": "date-balance",
    "ownership_transfer.document_transfer_date": "date-doc",
    "ownership_transfer.property_delivery_date": "date-delivery",
    "termination.penalty_amount": "penalty",
    "special_terms": "special-terms-box",
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
      seller: {
        name: getText(".seller-name"),
        id_number: getText(".seller-id"),
        address: getText(".seller-address"),
        contact: getText(".seller-contact"),
      },
      buyer: {
        name: getText(".buyer-name"),
        id_number: getText(".buyer-id"),
        address: getText(".buyer-address"),
        contact: getText(".buyer-contact"),
      },
      property: {
        location: getText(".property-location"),
        land_category: getText(".property-category"),
        land_area: getText(".property-area"),
        building_details: getText(".property-building"),
      },
      sale_price: {
        total_price: getText(".price-total"),
        down_payment: {
          amount: getText(".price-down"),
          payment_date: getText(".date-down"),
        },
        interim_payment: {
          amount: getText(".price-interim"),
          payment_date: getText(".date-interim"),
        },
        balance_payment: {
          amount: getText(".price-balance"),
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
      special_terms: getText(".special-terms-box"),
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 계약 당사자</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">매도인</td>
            <td>{renderField("seller-name", contract.seller?.name)}</td>
            <td>{renderField("seller-id", contract.seller?.id_number)}</td>
            <td>{renderField("seller-address", contract.seller?.address)}</td>
            <td>{renderField("seller-contact", contract.seller?.contact)}</td>
          </tr>
          <tr>
            <td className="gray">매수인</td>
            <td>{renderField("buyer-name", contract.buyer?.name)}</td>
            <td>{renderField("buyer-id", contract.buyer?.id_number)}</td>
            <td>{renderField("buyer-address", contract.buyer?.address)}</td>
            <td>{renderField("buyer-contact", contract.buyer?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 부동산 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">소재지</td>
            <td colSpan="3">{renderField("property-location", contract.property?.location)}</td>
          </tr>
          <tr>
            <td className="gray">지목</td>
            <td>{renderField("property-category", contract.property?.land_category)}</td>
            <td className="gray">면적</td>
            <td>{renderField("property-area", contract.property?.land_area)}㎡</td>
          </tr>
          <tr>
            <td className="gray">건물 내역</td>
            <td colSpan="3">{renderField("property-building", contract.property?.building_details)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 매매 대금</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">총액</td>
            <td colSpan="3">{renderField("price-total", contract.sale_price?.total_price)}</td>
          </tr>
          <tr>
            <td className="gray">계약금</td>
            <td>{renderField("price-down", contract.sale_price?.down_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-down", contract.sale_price?.down_payment?.payment_date)}</td>
          </tr>
          <tr>
            <td className="gray">중도금</td>
            <td>{renderField("price-interim", contract.sale_price?.interim_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-interim", contract.sale_price?.interim_payment?.payment_date)}</td>
          </tr>
          <tr>
            <td className="gray">잔금</td>
            <td>{renderField("price-balance", contract.sale_price?.balance_payment?.amount)}</td>
            <td className="gray">지급일</td>
            <td>{renderField("date-balance", contract.sale_price?.balance_payment?.payment_date)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 소유권 이전</p>
      <p className="contract-clause">
        매매 부동산에 대한 서류 이전일은 {renderField("date-doc", contract.ownership_transfer?.document_transfer_date)}, 부동산 인도일은 {renderField("date-delivery", contract.ownership_transfer?.property_delivery_date)}로 한다.
      </p>

      <p className="section-title">5. 계약 해제</p>
      <p className="contract-clause">계약 해제 시 위약금은 {renderField("penalty", contract.termination?.penalty_amount)} 원으로 한다.</p>

      <p className="section-title">6. 특약사항</p>
      <div className="special-terms-box">{renderField("special-terms-box", contract.special_terms)}</div>
    </div>
  );
});

export default SaleContract;
