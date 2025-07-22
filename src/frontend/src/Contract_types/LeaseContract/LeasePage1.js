import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const LeasePage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      property: {
        address: getText("property-address"),
        land_category: getText("property-category"),
        area: getText("property-area"),
        building_details: getText("property-building"),
      },
      lessor: {
        name: getText("lessor-name"),
        resident_number: getText("lessor-id"),
        address: getText("lessor-address"),
        contact: getText("lessor-contact"),
      },
      lessee: {
        name: getText("lessee-name"),
        resident_number: getText("lessee-id"),
        address: getText("lessee-address"),
        contact: getText("lessee-contact"),
      },
      lease_terms: {
        deposit: getText("lease-deposit"),
        monthly_rent: getText("lease-rent"),
        contract_period: {
          start_date: getText("lease-start"),
          end_date: getText("lease-end"),
        },
        payment_date: getText("lease-payment"),
      },
      management_fee: getText("management-fee"),
      use_purpose: getText("use-purpose"),
      delivery_date: getText("delivery-date"),
      termination: getText("termination"),
      special_terms: getText("special-terms-box"),
      real_estate_agent: {
        office_address: getText("agent-address"),
        office_name: getText("agent-office"),
        representative_name: getText("agent-rep"),
        registration_number: getText("agent-regnum"),
        broker_name: getText("agent-broker"),
      },
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

      <p className="section-title">1. 임대차 목적물</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">주소</td>
            <td>{renderField("property-address", contract.property?.address, suggestions)}</td>
            <td className="gray">지목</td>
            <td>{renderField("property-category", contract.property?.land_category, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">면적</td>
            <td>{renderField("property-area", contract.property?.area, suggestions)}㎡</td>
            <td className="gray">건물 내역</td>
            <td>{renderField("property-building", contract.property?.building_details, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 임대인 및 임차인 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">임대인</td>
            <td>{renderField("lessor-name", contract.lessor?.name, suggestions)}</td>
            <td>{renderField("lessor-id", contract.lessor?.resident_number, suggestions)}</td>
            <td>{renderField("lessor-address", contract.lessor?.address, suggestions)}</td>
            <td>{renderField("lessor-contact", contract.lessor?.contact, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">임차인</td>
            <td>{renderField("lessee-name", contract.lessee?.name, suggestions)}</td>
            <td>{renderField("lessee-id", contract.lessee?.resident_number, suggestions)}</td>
            <td>{renderField("lessee-address", contract.lessee?.address, suggestions)}</td>
            <td>{renderField("lessee-contact", contract.lessee?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 임대차 조건</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">보증금</td>
            <td>{renderField("lease-deposit", contract.lease_terms?.deposit, suggestions)}</td>
            <td className="gray">월세</td>
            <td>{renderField("lease-rent", contract.lease_terms?.monthly_rent, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">계약기간</td>
            <td>
              {renderField("lease-start", contract.lease_terms?.contract_period?.start_date, suggestions)} ~{" "}
              {renderField("lease-end", contract.lease_terms?.contract_period?.end_date, suggestions)}
            </td>
            <td className="gray">지급일</td>
            <td>{renderField("lease-payment", contract.lease_terms?.payment_date, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">4. 기타 조건</p>
      <p className="contract-clause">관리비: {renderField("management-fee", contract.management_fee, suggestions)}</p>
      <p className="contract-clause">용도: {renderField("use-purpose", contract.use_purpose, suggestions)}</p>
      <p className="contract-clause">인도일: {renderField("delivery-date", contract.delivery_date, suggestions)}</p>
      <p className="contract-clause">계약 해지 조건: {renderField("termination", contract.termination, suggestions)}</p>

      <p className="section-title">5. 특약사항</p>
      <div className="special-terms-box">{renderField("", contract.special_terms, suggestions)}</div>

      <p className="section-title">6. 중개업소 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">사무소명</td>
            <td>{renderField("agent-office", contract.real_estate_agent?.office_name, suggestions)}</td>
            <td className="gray">대표자</td>
            <td>{renderField("agent-rep", contract.real_estate_agent?.representative_name, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td>{renderField("agent-address", contract.real_estate_agent?.office_address, suggestions)}</td>
            <td className="gray">등록번호</td>
            <td>{renderField("agent-regnum", contract.real_estate_agent?.registration_number, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">공인중개사</td>
            <td colSpan="3">{renderField("agent-broker", contract.real_estate_agent?.broker_name, suggestions)}</td>
          </tr>
        </tbody>
      </table>
    </>
  );
});

export default LeasePage1;
