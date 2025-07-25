import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const EmploymentPage1 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      contract_type: getText("contract-main-title"),
      contract_date: getText("contract-date"),
      employer: {
        company_name: getText("employer-company"),
        representative_name: getText("employer-rep"),
        address: getText("employer-address"),
        contact: getText("employer-contact"),
      },
      employee: {
        name: getText("employee-name"),
        resident_number: getText("employee-id"),
        address: getText("employee-address"),
        contact: getText("employee-contact"),
      },
      employment_details: {
        position: getText("position"),
        duties: getText("duties"),
        workplace: getText("workplace"),
        contract_period: {
          start_date: getText("contract-start"),
          end_date: getText("contract-end"),
        },
        working_days: getText("working-days"),
        working_hours: {
          start_time: getText("work-start"),
          end_time: getText("work-end"),
          break_time: getText("break-time"),
        },
      },
      wage_details: {
        wage_type: getText("wage-type"),
        wage_amount: getText("wage-amount"),
        payment_date: getText("payment-date"),
        payment_method: getText("payment-method"),
        allowances: getText("allowances"),
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

      <p className="section-title">1. 사업주 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">회사명</td>
            <td>{renderField("employer-company", contract.employer?.company_name, suggestions)}</td>
            <td className="gray">대표자</td>
            <td>{renderField("employer-rep", contract.employer?.representative_name, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("employer-address", contract.employer?.address, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("employer-contact", contract.employer?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 근로자 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("employee-name", contract.employee?.name, suggestions)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("employee-id", contract.employee?.resident_number, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("employee-address", contract.employee?.address, suggestions)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("employee-contact", contract.employee?.contact, suggestions)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 근로 조건</p>
      <p className="contract-clause">직책: {renderField("position", contract.employment_details?.position, suggestions)}</p>
      <p className="contract-clause">업무 내용: {renderField("duties", contract.employment_details?.duties, suggestions)}</p>
      <p className="contract-clause">근무 장소: {renderField("workplace", contract.employment_details?.workplace, suggestions)}</p>
      <p className="contract-clause">계약 기간: {renderField("contract-start", contract.employment_details?.contract_period?.start_date, suggestions)}  <span className="nowrap"> ~ {renderField("contract-end", contract.employment_details?.contract_period?.end_date, suggestions)} </span></p>
      <p className="contract-clause">근무일: {renderField("working-days", contract.employment_details?.working_days, suggestions)}</p>
      <p className="contract-clause">근무 시간: {renderField("work-start", contract.employment_details?.working_hours?.start_time, suggestions)}<span className="nowrap"> ~ {renderField("work-end", contract.employment_details?.working_hours?.end_time, suggestions)}</span> (휴게시간: {renderField("break-time", contract.employment_details?.working_hours?.break_time, suggestions)})</p>

      <p className="section-title">4. 임금</p>
      <p className="contract-clause">임금 형태: {renderField("wage-type", contract.wage_details?.wage_type, suggestions)}</p>
      <p className="contract-clause">금액: {renderField("wage-amount", contract.wage_details?.wage_amount, suggestions)}</p>
      <p className="contract-clause">지급일: {renderField("payment-date", contract.wage_details?.payment_date, suggestions)}</p>
      <p className="contract-clause">지급 방법: {renderField("payment-method", contract.wage_details?.payment_method, suggestions)}</p>
      <p className="contract-clause">보조금: {renderField("allowances", contract.wage_details?.allowances, suggestions)}</p>


      <p className="section-title">5. 휴일 및 휴가</p>
      <p className="contract-clause">{renderField("holidays", contract.holidays, suggestions)}</p>
     
    </>
  );
});

export default EmploymentPage1;
