import React, { forwardRef, useImperativeHandle } from "react";
import { renderField } from "../utils";

const EmploymentPage2 = forwardRef(({ contract, suggestions }, ref) => {
  useImperativeHandle(ref, () => ({
    extract: () => ({
      other_terms: getText("other-terms"),
    }),
  }));

  const getText = (cls) => {
    const el = document.querySelector(`.${cls}`);
    return el?.dataset.suggestion === "true" ? "" : el?.innerText.trim() || "";
  };

  return (
    <>
      <p className="section-title">8. 기타사항</p>
      <div className="special-terms-box">{renderField("other-terms", contract.other_terms, suggestions)}</div>
    </>
  );
});

export default EmploymentPage2;