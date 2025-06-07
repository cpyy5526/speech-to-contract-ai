import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";
      
      const GiftPage2 = forwardRef(({ contract, suggestions }, ref) => {
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
            <p className="section-title">5. 서명란</p>
            <p className="signature-block">
                본 계약의 내용을 확인하고 이에 동의하여 아래와 같이 서명합니다.
            </p>

            <table className="contract-table" style={{ marginTop: "20px" }}>
                <tbody>
                <tr>
                    <td className="gray">증여자</td>
                    <td>{renderField("donor-sign", contract.donor?.name, suggestions)} (인)</td>
                </tr>
                <tr>
                    <td className="gray">수증자</td>
                    <td>{renderField("donee-sign", contract.donee?.name, suggestions)} (인)</td>
                </tr>
                </tbody>
            </table>

          </>
        );
      });
      
      export default GiftPage2;