import React, { forwardRef, useImperativeHandle, useRef, useState } from "react";
import LeasePage1 from "./LeasePage1";
import LeasePage2 from "./LeasePage2";
import "../Contract.css";
import { getPathToClass } from "../utils/pathToClass";
import { buildSuggestionMap } from "../utils";

const LeaseContract = forwardRef(({ contract, suggestions }, ref) => {
const [currentPage, setCurrentPage] = useState(0);

  const page1Ref = useRef();
  const page2Ref = useRef();
  const touchStartX = useRef(null);

  const pathToClass = getPathToClass(contract.contract_type);
  const suggestionMap = buildSuggestionMap(suggestions, pathToClass);

  const pages = [
    <div className="page" key="page1">
      <LeasePage1 ref={page1Ref} contract={contract} suggestions={suggestionMap} />
    </div>,
    <div className="page" key="page2">
      <LeasePage2 ref={page2Ref} contract={contract} suggestions={suggestionMap} />
    </div>,
  ];

   // 모바일 터치
  const handleTouchStart = (e) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e) => {
    if (touchStartX.current === null) return;
    const diffX = touchStartX.current - e.changedTouches[0].clientX;
    if (diffX > 50) setCurrentPage((p) => Math.min(p + 1, pages.length - 1));
    else if (diffX < -50) setCurrentPage((p) => Math.max(p - 1, 0));
    touchStartX.current = null;
  };


  // 버튼 조작
  const handlePrev = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 0));
  };

  const handleNext = () => {
    setCurrentPage((prev) => Math.min(prev + 1, pages.length - 1));
  };

  useImperativeHandle(ref, () => ({
    extract: () => {
      const data1 = page1Ref.current?.extract?.() || {};
      const data2 = page2Ref.current?.extract?.() || {};
      return { ...data1, ...data2 };
    },
  }));

  return (
    <div className="slider-wrapper">
      <div
        className="slider-container"
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        <div
          className="slider"
          style={{ transform: `translateX(-${currentPage * 100}%)` }}
        >
          {pages.map((page) => (
            <div className="slide" key={page.key}>
              {page}
            </div>
          ))}
        </div>
      </div>

      {/* PC 버튼 및 페이지 인디케이터 */}
      <div className="slider-controls">
        <button onClick={handlePrev} disabled={currentPage === 0}>◀</button>
        <span>{currentPage + 1} / {pages.length}</span>
        <button onClick={handleNext} disabled={currentPage === pages.length - 1}>▶</button>
      </div>
    </div>
  );
});

export default LeaseContract;
