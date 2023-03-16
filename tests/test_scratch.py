import sys
sys.path.append("..")
from database.DBconn import pullPremiumTable
from scratch import main
from scratch.firm_code import firm_code

premiums = main.Scratch_GP_File(firm_code['204'], '微馨彩')
pullPremiumTable(premiums)