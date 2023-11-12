import itertools
from config import *
import json
import os
import requests


class PlayScore():
	def __init__(self):
		self.local_file_path = os.path.join(os.path.dirname(__file__), MEASURES_FILE_NAME)
		try:
			with open(self.local_file_path) as fp:
				self.measures_list = json.load(fp)
		except FileNotFoundError:
			self.measures_list = []
	
	@staticmethod
	def ingest_risks():
		error_msg = ""
		url = BASE_URL + "/risk"
		params = {
			"token": AUTHENTICATION_TOKEN
		}
		headers = {
			'Content-Type': 'application/json'
		}
		response = requests.request("GET", url, headers=headers, params=params)
		if response.status_code != 200:
			risks_list = []
			error_msg = response.text
		else:
			risks_list = response.json()
		return risks_list, error_msg
	
	@staticmethod
	def play_score(comb_ids_list):
		url = BASE_URL + "/play"
		params = {
			"token": AUTHENTICATION_TOKEN
		}
		headers = {
			'Content-Type': 'application/json'
		}
		payload = json.dumps({
			"measures": comb_ids_list
		})
		response = requests.request("POST", url, headers=headers, params=params, data=payload)
		return response
	
	def get_combinations_score(self, combinations):
		combinations_score_dict = dict()
		risks_list, error_msg = self.ingest_risks()
		if not risks_list:
			return {}, error_msg
		global_severity = sum(item.get("severity") for item in risks_list)
		for comb in combinations:
			total_risk_coverage_dict = dict()
			global_score = 0
			global_cost = sum(item['cost'] for item in comb)
			for risk in risks_list:
				total_risk_coverage = 0
				for measure in comb:
					try:
						rr = [element for element in measure.get("riskCoverage") 
								if element.get("risk") == risk.get("identifier")
							 ][0]
					except:
						continue
					total_risk_coverage += rr.get("coverage")
				severity = risk.get("severity")
				total_risk_coverage_dict[risk.get("identifier")] = {
						"coverage" : total_risk_coverage,
						"severity": severity
				}
				global_score += total_risk_coverage * severity

			score_returned = round(global_score / global_severity, 2)
			measures_ids = [item.get("identifier") for item in comb]
			combinations_score_dict['/'.join(measures_ids)] = {"score": score_returned, "cost": global_cost, "risks": total_risk_coverage_dict}
		return combinations_score_dict, error_msg

	def get_best_combination_ids(self):
		combinations = list(itertools.combinations(self.measures_list, COMBINATION_LENGTH))
		if not combinations:
			return [], f"Measure data not loaded correctly from local file. Please check the path: {self.local_file_path}"
		combinations_score_dict, error_msg = self.get_combinations_score(combinations)
		if not combinations_score_dict:
			return [], error_msg
		max_score_under_budget = max([value.get("score") for value in combinations_score_dict.values() if value.get("cost") <= COST_LIMIT])
		comb_with_max_score_under_budget = [key for key, value in combinations_score_dict.items() if value.get("score") == max_score_under_budget]

		if len(comb_with_max_score_under_budget) > 1:
			# getting the combination with the lowest cost in case of the same max score
			comb_with_max_score_under_budget = [key for key,value in combinations_score_dict.items() 
											  		if value.get("cost") == min([combinations_score_dict.get(id).get("cost") for id in comb_with_max_score_under_budget]) 
													and value.get("score")==max_score_under_budget
												]
		try:
			# selecting the first combination in case of multiple ones with max_score and min_cost (already under budget)
			ids_list = comb_with_max_score_under_budget[0].split('/')
		except IndexError:
			ids_list = []
			error_msg = f"No combination found respecting the budget of {COST_LIMIT}"
		return ids_list, error_msg


if __name__ == '__main__':
	#'MEAS-28/MEAS-25/MEAS-32': max_score = 95.7 ; cost > 100 (budget)
	#'MEAS-25/MEAS-28/MEAS-19': max_score_under_budget = 86.5 (check the data used by /play API because it returns 80.4) ; cost = 96 
	
	comb_ids_list, error_msg = PlayScore().get_best_combination_ids()
	if not comb_ids_list:
		print(error_msg)
	else:
		play_response = PlayScore().play_score(comb_ids_list)
		response_text = "Played combination: " + str(comb_ids_list) + '\n'
		if play_response.status_code == 200:
			if play_response.json().get('score'):
				response_text += f"Score: {play_response.json().get('score')}"
			else:
				response_text += f"Response: {play_response.json()}"
		else:
			response_text += f"Error: {play_response.text}"
		print(response_text)
