const pathToClass = (path) => ({
  "loan_amount.amount_korean": "loan-amount-kor",
  "loan_amount.amount_number": "loan-amount-num",

  "interest.rate": "interest-rate",
  "interest.payment_method": "interest-method",
  "interest.payment_date": "interest-date",

  "repayment.repayment_date": "repayment-date",
  "repayment.account_info": "repayment-account",
}[path]);

export default pathToClass;
