import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const ExchangePage2 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      special_terms: getText("special-terms-box"),
      signature_and_seal: "서명 완료"
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <>
      <p className="section-title">7. 특약사항</p>
      <div className="special-terms-box">
        {renderField("", contract.special_terms, suggestions)}
      </div>

      <p className="section-title">8. 서명란</p>
      <p className="signature-block">
        본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
      </p>

      <table className="contract-table" style={{ marginTop: "20px" }}>
        <tbody>
          <tr>
            <td className="gray">갑</td>
            <td>{renderField("partyA-sign", contract.party_A?.name, suggestions)} (인)</td>
          </tr>
          <tr>
            <td className="gray">을</td>
            <td>{renderField("partyB-sign", contract.party_B?.name, suggestions)} (인)</td>
          </tr>
        </tbody>
      </table>
    </>
  );
});

export default ExchangePage2;
