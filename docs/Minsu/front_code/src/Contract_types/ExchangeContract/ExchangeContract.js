import React, { forwardRef, useImperativeHandle, useRef } from "react";
import ExchangePage1 from "./ExchangePage1";
import ExchangePage2 from "./ExchangePage2";
import "../Contract.css";
import { getPathToClass } from "../utils/pathToClass";
import { buildSuggestionMap } from "../utils";

const ExchangeContract = forwardRef(({ contract, suggestions }, ref) => {
  const page1Ref = useRef();
  const page2Ref = useRef();

  const pathToClass = getPathToClass(contract.contract_type);
  const suggestionMap = buildSuggestionMap(suggestions, pathToClass);

  useImperativeHandle(ref, () => ({
    extract: () => {
      const data1 = page1Ref.current?.extract?.() || {};
      const data2 = page2Ref.current?.extract?.() || {};
      return { ...data1, ...data2 };
    },
  }));

  return (
    <div className="pdf-container">
      <div className="page">
        <ExchangePage1 ref={page1Ref} contract={contract} suggestions={suggestionMap} />
      </div>

      <div className="page">
        <ExchangePage2 ref={page1Ref} contract={contract} suggestions={suggestionMap} />
      </div>
    </div>
  );
});

export default ExchangeContract;