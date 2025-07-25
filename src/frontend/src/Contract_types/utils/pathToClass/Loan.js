const pathToClass = (path) => ({
  "contract-date": "contract-date",
  
  "loan_amount.amount_korean": "loan-korean",
  "loan_amount.amount_number": "loan-number",

  "interest.rate": "interest-rate",
  "interest.payment_method": "interest-method",
  "interest.payment_date": "interest-date",

  "repayment.repayment_date": "repay-date",
  "repayment.account_info": "repay-account",
}[path]);

export default pathToClass;
