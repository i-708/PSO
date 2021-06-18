def csv_writer():
    import datetime
    import new_pso

    # 現在の日時を取得
    now = datetime.datetime.now()

    # ファイル名の生成
    file_name = now.strftime('%Y%m%d_%H%M%S') + '.csv'

    # pathの生成
    path = 'PSO/new-pso-prog/result/' + file_name

    with open(path, mode='w') as f:
        f.write(file_name)


csv_writer()
