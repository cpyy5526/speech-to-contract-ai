const pathToClass = (path) => ({
  "employment_details.duties": "job-duties",
  "employment_details.workplace": "job-workplace",
  "employment_details.contract_period.start_date": "job-start",
  "employment_details.contract_period.end_date": "job-end",
  "employment_details.working_days": "job-days",
  "employment_details.working_hours.start_time": "job-start-time",
  "employment_details.working_hours.end_time": "job-end-time",

  "wage_details.wage_type": "wage-type",
  "wage_details.wage_amount": "wage-amount",
  "wage_details.payment_date": "wage-date",
  "wage_details.payment_method": "wage-method",

  "termination": "termination",
}[path]);

export default pathToClass;
