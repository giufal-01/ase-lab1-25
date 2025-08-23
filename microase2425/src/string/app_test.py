import app as main_app

flask_app = main_app.app

def mock_save_last(op,args,res):
    print(f"Mock save_last: {op} {args} {res}")

main_app.mock_save_last = mock_save_last 