import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const ConstructionPage2 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      signature_and_seal: "서명 완료", // 필요 시 필드 추가
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <>
      <p className="section-title">8. 특약사항</p>
        <div className="special-terms-box">
            {renderField("special-terms-box", contract.special_terms, suggestions)}
        </div>

      <p className="section-title">9. 서명란</p>
      <p className="signature-block">
        본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
      </p>

      <table className="contract-table" style={{ marginTop: "20px" }}>
        <tbody>
          <tr>
            <td className="gray">도급인</td>
            <td>{renderField("contractee-sign", contract.contractee?.name, suggestions)} (인)</td>
          </tr>
          <tr>
            <td className="gray">수급인</td>
            <td>{renderField("contractor-sign", contract.contractor?.name, suggestions)} (인)</td>
          </tr>
        </tbody>
      </table>
    </>
  );
});

export default ConstructionPage2;
