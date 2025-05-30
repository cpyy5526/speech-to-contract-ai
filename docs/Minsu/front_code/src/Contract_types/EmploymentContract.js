import React, { forwardRef, useImperativeHandle } from "react";
import "./GiftContract.css";

const EmploymentContract = forwardRef(({ contract, suggestions = [] }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: extractEditedContents,
  }));

  

  const pathToClass = (path) => ({
    "contract_type": "contract-main-title",
    "contract_date": "contract-date",
    "employer.company_name": "employer-company",
    "employer.representative_name": "employer-rep",
    "employer.address": "employer-address",
    "employer.contact": "employer-contact",
    "employee.name": "employee-name",
    "employee.resident_number": "employee-id",
    "employee.address": "employee-address",
    "employee.contact": "employee-contact",
    "employment_details.position": "position",
    "employment_details.duties": "duties",
    "employment_details.workplace": "workplace",
    "employment_details.contract_period.start_date": "contract-start",
    "employment_details.contract_period.end_date": "contract-end",
    "employment_details.working_days": "working-days",
    "employment_details.working_hours.start_time": "work-start",
    "employment_details.working_hours.end_time": "work-end",
    "employment_details.working_hours.break_time": "break-time",
    "wage_details.wage_type": "wage-type",
    "wage_details.wage_amount": "wage-amount",
    "wage_details.payment_date": "payment-date",
    "wage_details.payment_method": "payment-method",
    "holidays": "holidays",
    "social_insurance.national_pension": "social-pension",
    "social_insurance.health_insurance": "social-health",
    "social_insurance.employment_insurance": "social-employment",
    "social_insurance.industrial_accident_insurance": "social-accident",
    "termination": "termination",
    "other_terms": "other-terms",
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
      employer: {
        company_name: getText(".employer-company"),
        representative_name: getText(".employer-rep"),
        address: getText(".employer-address"),
        contact: getText(".employer-contact"),
      },
      employee: {
        name: getText(".employee-name"),
        resident_number: getText(".employee-id"),
        address: getText(".employee-address"),
        contact: getText(".employee-contact"),
      },
      employment_details: {
        position: getText(".position"),
        duties: getText(".duties"),
        workplace: getText(".workplace"),
        contract_period: {
          start_date: getText(".contract-start"),
          end_date: getText(".contract-end"),
        },
        working_days: getText(".working-days"),
        working_hours: {
          start_time: getText(".work-start"),
          end_time: getText(".work-end"),
          break_time: getText(".break-time"),
        },
      },
      wage_details: {
        wage_type: getText(".wage-type"),
        wage_amount: getText(".wage-amount"),
        payment_date: getText(".payment-date"),
        payment_method: getText(".payment-method"),
      },
      holidays: getText(".holidays"),
      social_insurance: {
        national_pension: getText(".social-pension") === "O",
        health_insurance: getText(".social-health") === "O",
        employment_insurance: getText(".social-employment") === "O",
        industrial_accident_insurance: getText(".social-accident") === "O",
      },
      termination: getText(".termination"),
      other_terms: getText(".other-terms"),
      signature_and_seal: getText(".sign-seal"),
    };
  };

  return (
    <div className="gift-contract">
      <h1 className="contract-main-title">{renderField("contract-main-title", contract.contract_type)}</h1>
      <p className="contract-date">{renderField("contract-date", contract.contract_date)}</p>

      <p className="section-title">1. 사업주 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">회사명</td>
            <td>{renderField("employer-company", contract.employer?.company_name)}</td>
            <td className="gray">대표자</td>
            <td>{renderField("employer-rep", contract.employer?.representative_name)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("employer-address", contract.employer?.address)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("employer-contact", contract.employer?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">2. 근로자 정보</p>
      <table className="contract-table">
        <tbody>
          <tr>
            <td className="gray">성명</td>
            <td>{renderField("employee-name", contract.employee?.name)}</td>
            <td className="gray">주민등록번호</td>
            <td>{renderField("employee-id", contract.employee?.resident_number)}</td>
          </tr>
          <tr>
            <td className="gray">주소</td>
            <td colSpan="3">{renderField("employee-address", contract.employee?.address)}</td>
          </tr>
          <tr>
            <td className="gray">연락처</td>
            <td colSpan="3">{renderField("employee-contact", contract.employee?.contact)}</td>
          </tr>
        </tbody>
      </table>

      <p className="section-title">3. 근로 조건</p>
      <p className="contract-clause">직책: {renderField("position", contract.employment_details?.position)}</p>
      <p className="contract-clause">업무 내용: {renderField("duties", contract.employment_details?.duties)}</p>
      <p className="contract-clause">근무 장소: {renderField("workplace", contract.employment_details?.workplace)}</p>
      <p className="contract-clause">계약 기간: {renderField("contract-start", contract.employment_details?.contract_period?.start_date)} ~ {renderField("contract-end", contract.employment_details?.contract_period?.end_date)}</p>
      <p className="contract-clause">근무일: {renderField("working-days", contract.employment_details?.working_days)}</p>
      <p className="contract-clause">근무 시간: {renderField("work-start", contract.employment_details?.working_hours?.start_time)} ~ {renderField("work-end", contract.employment_details?.working_hours?.end_time)} (휴게시간: {renderField("break-time", contract.employment_details?.working_hours?.break_time)})</p>

      <p className="section-title">4. 임금</p>
      <p className="contract-clause">임금 형태: {renderField("wage-type", contract.wage_details?.wage_type)}</p>
      <p className="contract-clause">금액: {renderField("wage-amount", contract.wage_details?.wage_amount)}</p>
      <p className="contract-clause">지급일: {renderField("payment-date", contract.wage_details?.payment_date)}</p>
      <p className="contract-clause">지급 방법: {renderField("payment-method", contract.wage_details?.payment_method)}</p>

      <p className="section-title">5. 휴일 및 휴가</p>
      <p className="contract-clause">{renderField("holidays", contract.holidays)}</p>

      <p className="section-title">6. 4대 보험 가입 여부 (O/X)</p>
      <p className="contract-clause">국민연금: {renderField("social-pension", contract.social_insurance?.national_pension ? "O" : "X")}, 건강보험: {renderField("social-health", contract.social_insurance?.health_insurance ? "O" : "X")}, 고용보험: {renderField("social-employment", contract.social_insurance?.employment_insurance ? "O" : "X")}, 산재보험: {renderField("social-accident", contract.social_insurance?.industrial_accident_insurance ? "O" : "X")}</p>

      <p className="section-title">7. 해고 및 계약해지</p>
      <p className="contract-clause">{renderField("termination", contract.termination)}</p>

      <p className="section-title">8. 기타사항</p>
      <div className="special-terms-box">{renderField("other-terms", contract.other_terms)}</div>
    </div>
  );
});

export default EmploymentContract;
