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
  const isEmptyContent = !content || content === "________";
  const displayText = !content ? suggestion || "________" : content;
  const style = !content
    ? suggestion
      ? { color: "#888" }
      : { color: "#ccc" }
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

  return (
    <span
      className={className}
      contentEditable
      suppressContentEditableWarning
      style={style}
      data-suggestion={isEmptyContent && suggestion ? "true" : "false"}
      onInput={handleInput}
    >
      {typeof displayText === "string" ? displayText : String(displayText)}
    </span>
  );
};

