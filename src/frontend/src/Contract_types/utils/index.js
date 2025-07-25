export const buildSuggestionMap = (suggestions, pathToClassFn) => {
  const suggestionMap = {};

  const baseSuggestions = [
    { field_path: "contract-date", suggestion_text: "날짜를 입력해주세요" },
  ];

  const allSuggestions = [...baseSuggestions, ...suggestions];

  allSuggestions.forEach(({ field_path, suggestion_text }) => {
    const className = pathToClassFn(field_path);
    if (className) suggestionMap[className] = suggestion_text;
  });
  return suggestionMap;
};

export const renderField = (className, content, suggestionMap = {}) => {
  const suggestion = suggestionMap[className];
  const isPlaceholder = !content || content === "________";
  const displayText = !content ? suggestion || "________" : content;
  const style = !content
    ? suggestion
      ? { color: "#888" }
      : { color: "#ccc" }
    : content === "________"
      ? { color: "#ccc" }
      : {};

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

  const handleBlur = (e) => {
    const el = e.currentTarget;
    if (el.innerText.trim() === "") {
      el.innerText = "________";
      el.dataset.suggestion = "true";
      el.style.color = "#ccc";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault(); // 줄바꿈 방지
      e.currentTarget.blur(); // 입력 종료
    }
  };

  return (
    <span
      className={className}
      contentEditable
      suppressContentEditableWarning
      style={style}
      data-suggestion={isPlaceholder ? "true" : "false"}
      onInput={handleInput}
      onBlur={handleBlur}
      onKeyDown={handleKeyDown}
    >
      {typeof displayText === "string" ? displayText : String(displayText)}
    </span>
  );
};


