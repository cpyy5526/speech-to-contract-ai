import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const EmploymentPage2 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      holidays: getText("holidays"),
      social_insurance: {
        national_pension: getText("social-pension") === "O",
        health_insurance: getText("social-health") === "O",
        employment_insurance: getText("social-employment") === "O",
        industrial_accident_insurance: getText("social-accident") === "O",
      },
      termination: getText("termination"),
      other_terms: getText("other-terms"),
      signature_and_seal: "서명 완료" // or 다른 처리 방식
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <>
      <p className="section-title">6. 4대 보험 가입 여부 (O/X)</p>
      <p className="contract-clause">
        국민연금: {renderField("social-pension", contract.social_insurance?.national_pension ? "O" : "X", suggestions)},
        건강보험: {renderField("social-health", contract.social_insurance?.health_insurance ? "O" : "X", suggestions)},
        고용보험: {renderField("social-employment", contract.social_insurance?.employment_insurance ? "O" : "X", suggestions)},
        산재보험: {renderField("social-accident", contract.social_insurance?.industrial_accident_insurance ? "O" : "X", suggestions)}
      </p>
      
      <p className="section-title">7. 해고 및 계약해지</p>
      <p className="contract-clause">{renderField("termination", contract.termination, suggestions)}</p>

      <p className="section-title">8. 기타사항</p>
      <div className="special-terms-box">
        {renderField("other-terms", contract.other_terms, suggestions)}
      </div>

      <p className="section-title">9. 서명란</p>
      <p className="signature-block">
        본 계약의 내용을 확인하고 이에 동의하여 아래에 서명합니다.
      </p>

      <table className="contract-table" style={{ marginTop: "20px" }}>
        <tbody>
          <tr>
            <td className="gray">사업주</td>
            <td>{renderField("employer-sign", contract.employer?.representative_name, suggestions)} (인)</td>
          </tr>
          <tr>
            <td className="gray">근로자</td>
            <td>{renderField("employee-sign", contract.employee?.name, suggestions)} (인)</td>
          </tr>
        </tbody>
      </table>
    </>
  );
});

export default EmploymentPage2;
