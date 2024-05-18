import configparser

#function for creating the configuration file
def createFile(filePath):
    config = configparser.ConfigParser()
    
    #adding categories and settings to the created ini file
    config['categoryOne'] = {'settingOne': 'True', 'settingTwo': 'False', 'settingThree': 'False'}
    config['categoryTwo'] = {'settingOne': 'True', 'settingTwo': 'True', 'settingThree': 'True'}
    
    #writing the configurations to the ini file
    with open(filePath, 'w') as configFile:
        config.write(configFile)

#function for editing the configuration file
def updateFile(filePath, configCategory, configSetting, configValue):
    config = configparser.ConfigParser()
    config.read(filePath)
  
    #changing the value in the file
    if not config.has_section(configCategory):
        config.add_section(configCategory)
    config.set(configCategory, configSetting, configValue)
    
    #writing the changes made back to the file
    with open(filePath, 'w') as configfile:
        config.write(configfile)