import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from fuzzylogic.fuzzycode import timemachine
from fuzzylogic.fuzzycode import zscore
from fuzzylogic.fuzzycode import scamchecker

from fuzzylogic.fuzzycode import logfile_data_extractor

def main(log_filepath):
    # Antecedents (Inputs)
    receiver_address = ctrl.Antecedent(np.arange(0, 4, 1), 'receiver_address')
    time_deviation = ctrl.Antecedent(np.arange(0, 101, 1), 'time_deviation')
    ether_value = ctrl.Antecedent(np.arange(0, 101, 1), 'ether_value')

    # Membership functions for receiver address
    receiver_address['Low'] = fuzz.trimf(receiver_address.universe, [0, 0, 1])
    receiver_address['Medium'] = fuzz.trimf(receiver_address.universe, [1, 1, 2])
    receiver_address['High'] = fuzz.trimf(receiver_address.universe, [2, 2, 3])
    receiver_address['Very High'] = fuzz.trimf(receiver_address.universe, [3, 3, 3])

    # Membership functions for time deviation
    time_deviation['Very Small'] = fuzz.trimf(time_deviation.universe, [0, 0, 25])
    time_deviation['Small'] = fuzz.trimf(time_deviation.universe, [0, 25, 50])
    time_deviation['Medium'] = fuzz.trimf(time_deviation.universe, [25, 50, 75])
    time_deviation['Large'] = fuzz.trimf(time_deviation.universe, [50, 75, 100])
    time_deviation['Very Large'] = fuzz.trimf(time_deviation.universe, [75, 100, 100])

    # Membership functions for ether value
    ether_value['Very Low'] = fuzz.trimf(ether_value.universe, [0, 0, 25])
    ether_value['Low'] = fuzz.trimf(ether_value.universe, [0, 25, 50])
    ether_value['Medium'] = fuzz.trimf(ether_value.universe, [25, 50, 75])
    ether_value['High'] = fuzz.trimf(ether_value.universe, [50, 75, 100])
    ether_value['Very High'] = fuzz.trimf(ether_value.universe, [75, 100, 100])

    # Consequent (Output)
    risk_level = ctrl.Consequent(np.arange(0, 101, 1), 'risk_level')

    # Membership functions for risk level
    risk_level['Very Low'] = fuzz.trimf(risk_level.universe, [0, 0, 25])
    risk_level['Low'] = fuzz.trimf(risk_level.universe, [0, 25, 50])
    risk_level['Medium'] = fuzz.trimf(risk_level.universe, [25, 50, 75])
    risk_level['High'] = fuzz.trimf(risk_level.universe, [50, 75, 100])
    risk_level['Very High'] = fuzz.trimf(risk_level.universe, [75, 100, 100])

    # Define fuzzy rules
    rule1 = ctrl.Rule(receiver_address['Low'] & time_deviation['Very Small'] & ether_value['Very Low'], risk_level['Very Low'])
    rule2 = ctrl.Rule(receiver_address['Medium'] & time_deviation['Small'] & ether_value['Low'], risk_level['Low'])
    rule3 = ctrl.Rule(receiver_address['High'] & time_deviation['Medium'] & ether_value['Medium'], risk_level['Medium'])
    rule4 = ctrl.Rule(receiver_address['Very High'] & time_deviation['Large'] & ether_value['High'], risk_level['High'])
    rule5 = ctrl.Rule(receiver_address['Very High'] & time_deviation['Very Large'] & ether_value['Very High'], risk_level['Very High'])

    # Control system creation and simulation
    risk_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    risk_assessment = ctrl.ControlSystemSimulation(risk_control)
    
    data = logfile_data_extractor.extract_data(log_filepath)
    
    
    
    risk_assessment.input['receiver_address'] = scamchecker.account_risk(data["to"])
    risk_assessment.input['time_deviation'] = timemachine.check_user_pattern_deviation(data["from"], data["timestamp"])
    risk_assessment.input['ether_value'] = zscore.ether_analyzer(data["from"], data["value"])
    
    # risk_assessment.input['receiver_address'] = scamchecker.account_risk()
    # risk_assessment.input['time_deviation'] = timemachine.check_user_pattern_deviation(1,2)
    # risk_assessment.input['ether_value'] = zscore.ether_analyzer(1,2)
    
    print(type(scamchecker.account_risk()))
    print(type(timemachine.check_user_pattern_deviation(1,2)))
    print(type(zscore.ether_analyzer(1,2)))

    # Perform the simulation
    risk_assessment.compute()

    # The result is a fuzzy risk level percentage
    risk_level_result = risk_assessment.output['risk_level']
    return risk_level_result, data