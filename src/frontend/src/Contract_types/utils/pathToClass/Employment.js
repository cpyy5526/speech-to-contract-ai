const pathToClass = (path) => ({
  "employment_details.duties": "duties",
  "employment_details.workplace": "workplace",
  "employment_details.contract_period.start_date": "contract-start",
  "employment_details.contract_period.end_date": "contract-end",
  "employment_details.working_days": "working-days",
  "employment_details.working_hours.start_time": "work-start",
  "employment_details.working_hours.end_time": "work-end",

  "wage_details.wage_type": "wage-type",
  "wage_details.wage_amount": "wage-amount",
  "wage_details.payment_date": "payment-date",
  "wage_details.payment_method": "payment-method",

  "termination": "termination",
}[path]);

export default pathToClass;
