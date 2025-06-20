export const buildSuggestionMap = (suggestions, pathToClassFn) => {
  const suggestionMap = {};
  suggestions.forEach(({ field_path, suggestion_text }) => {
    const className = pathToClassFn(field_path);
    if (className) suggestionMap[className] = suggestion_text;
  });
  return suggestionMap;
};


export const renderField = (className, content, suggestionMap = {}) => {
  const suggestion = suggestionMap[className];
  const displayText = content || suggestion || "________";
  const style = content ? {} : suggestion ? { color: "#888" } : { color: "#ccc" };

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
      data-suggestion={content ? "false" : suggestion ? "true" : "false"}
      onInput={handleInput}
    >
      {typeof displayText === "string" ? displayText : String(displayText)}
    </span>
  );
};

