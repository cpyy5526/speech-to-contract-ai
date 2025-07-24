import gift from "./Gift";
import lease from "./Lease";
import loan from "./Loan";
import sale from "./Sale";
import exchange from "./Exchange";
import employment from "./Employment";
import construction from "./Construction";
import usageLoan from "./UsageLoan";

const pathMap = {
  "증여 계약": gift,
  "임대차 계약": lease,
  "금전 대여 계약": loan,
  "매매 계약": sale,
  "교환 계약": exchange,
  "고용": employment,
  "공사 계약": construction,
  "사용대차 계약": usageLoan,
};

/**
 * contract_type 문자열에 따라 해당 pathToClass 함수 반환
 * @param {string} contractType
 * @returns {(path: string) => string | undefined}
 */
export const getPathToClass = (contractType) => pathMap[contractType] || (() => undefined);
