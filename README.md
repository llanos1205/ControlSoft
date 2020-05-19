# ControlSoft
Home-Urbanization-Department-Local management (AWS lambda integration)
python3.7 based
##parts:
###auth package:
  contains basic authentication sing_in/log_in/password change etc. with AWS Cognito user pools
###libpacks:
  contains the basic lib needed as a lambda layer for postgresql and/or mysql support
###restpackage:
  contains .py files needed as a lambda layer for db operations and lambdaproxy integration responses with API gateway
