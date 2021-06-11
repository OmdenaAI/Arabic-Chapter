import time
from selenium import webdriver

driver = None
def get_pos(sentence):
    global driver
    try:
        text_area = driver.find_element_by_id('ex_textbox')
        text_area.send_keys(sentence)
        time.sleep(1)
        element = driver.find_elements_by_class_name('v-select-select')
        for option in element[1].find_elements_by_tag_name('option'):
            if option.text == 'Parts-of-Speech':
                option.click()
        time.sleep(1)
        segments = driver.find_elements_by_class_name('segment')
        sentence_data = {}
        for segment in segments:
            for analysis in segment.find_elements_by_tag_name('a'):
                word = analysis.find_element_by_class_name('word')
                word = word.find_element_by_tag_name('ul')
                word = word.find_element_by_class_name('o')
                word = word.text
                pos = analysis.find_element_by_class_name('tip')
                pos = pos.find_element_by_class_name('m-pos')
                pos = pos.find_element_by_tag_name('span')
                pos = pos.get_attribute("innerHTML")
                sentence_data[word] = pos
        time.sleep(2)
        text_area.clear()
        return sentence_data
    except:
        print('Error in  getting POS from MADAMIRA')
        driver.quit()
        return []

def evaluate(sentence, pred_tags):
    global driver
    driver = webdriver.Edge(r'E:\Omdena\Arabic_Language_NLP\task-10-dataset-collection\mlp_data\msedgedriver.exe')
    driver.get('https://camel.abudhabi.nyu.edu/madamira/')
    time.sleep(4)
    true_tags = get_pos(sentence)
    driver.quit()
    acc = 0
    for i in pred_tags:
        try:
            if true_tags[i[0]].lower().replace(' ','') == i[1]:
                acc+=1
        except:continue
    return acc *100.0 /len(pred_tags)
    
