import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";
      
      const LeasePage2 = forwardRef(({ contract, suggestions }, ref) => {
        useImperativeHandle(ref, () => ({
          extract: () => ({
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
            <p className="section-title">7. 서명란</p>
            <p className="signature-block">
            본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
            </p>

            <table className="contract-table" style={{ marginTop: "20px" }}>
            <tbody>
                <tr>
                <td className="gray">임대인</td>
                <td>{renderField("lessor-sign", contract.lessor?.name, suggestions)} (인)</td>
                </tr>
                <tr>
                <td className="gray">임차인</td>
                <td>{renderField("lessee-sign", contract.lessee?.name, suggestions)} (인)</td>
                </tr>
            </tbody>
            </table>

          </>
        );
      });
      
      export default LeasePage2;