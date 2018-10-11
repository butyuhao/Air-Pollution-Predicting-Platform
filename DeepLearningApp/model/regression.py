import numpy as np
np.random.seed(1337)  # for reproducibility
from django.http import JsonResponse
import json
import keras
from django.views.decorators.http import require_http_methods
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt # 可视化模块
import pymysql
from math import sqrt
import scipy.stats.stats as stats
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense
from keras import optimizers
from sklearn.metrics import mean_squared_error

@require_http_methods(["GET"])
def startTraing(request):
    response = {}
    model = request.GET.get("model")
    dataset = request.GET.get("dataset")
    if(model == "regression"):
        weight = request.GET.get('weight')
        bias = request.GET.get("bias")

        cnx = pymysql.connect(user='root', password='butyuhao',
                              host='127.0.0.1',
                              database='DeepLearningArchitecture')
        cursor = cnx.cursor()
        sql = "select * from regression"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        tmpX = []
        tmpY = []
        for row in results:
            tmpX.append(row[1])
            tmpY.append(row[2])
        cursor.close()
        cnx.close()
        X = np.array(tmpX, dtype=np.float64)
        # Y = np.array(tmpY, dtype=np.float64)
        Y = float(weight) * X + float(bias) + np.random.normal(0, 0.05, (200,))

        # Y = weight * X + bias + np.random.normal(0, 0.05, (200,))
        X_train, Y_train = X[:160], Y[:160]  # train 前 160 data points
        X_test, Y_test = X[160:], Y[160:]  # test 后 40 data points
        keras.backend.clear_session()
        model = Sequential()
        model.add(Dense(output_dim=1, input_dim=1))
        model.compile(loss='mse', optimizer='sgd')

        trainingCost = 0
        testingCost = 0
        rows = []
        columns = ['number', 'TrainLoss']
        print('Training.......')
        for i in range(301):
            cost = model.train_on_batch(X_train, Y_train)
            if i % 10 == 0:
                tmp = {}
                # print('train cost:', cost)
                tmp['number'] = str(i)
                tmp['TrainLoss'] = float(cost)
                rows.append(tmp)
            trainingCost = float(cost)

        # test
        print('\nTesting ------------')
        testingCost = model.evaluate(X_test, Y_test, batch_size=40)
        print('www cost:', testingCost)
        W, b = model.layers[0].get_weights()
        print('Weights=', W, '\nbiases=', b)

        Y_pred = model.predict(X_test)

        error = []
        for i in range(len(Y_test)):
            error.append(Y_test[i] - Y_pred[i])

        squaredError = []
        for val in error:
            squaredError.append(val * val)  # target-prediction之差平方

        RMSE = sqrt(sum(squaredError) / len(squaredError))
        pearsonr = stats.pearsonr(X, Y)[0]

        modelParameters = {}
        modelParameters['Weight'] = weight
        modelParameters['Bias'] = bias
        modelParameters['TotalSize'] = X.size
        modelParameters['TrainSize'] = X.size * 0.8
        modelParameters['TestSize'] = Y.size * 0.2
        modelParameters['Model'] = "Regression"

        resultData = {}
        resultData['columns'] = columns
        resultData['rows'] = rows

        resultStatic = {}
        resultStatic['trainingCost'] = float(trainingCost)
        resultStatic['testingCost'] = testingCost
        resultStatic['RMSE'] = float(RMSE)
        resultStatic['pearsonr'] = float(pearsonr)

        ResultDatatmp = {}

        response['ResultData'] = ResultDatatmp
        response['ResultData2'] = resultData
        response['resultStatic'] = resultStatic
        response['modelParameters'] = modelParameters
        response['msg'] = 'success'
        response['error_num'] = 0

    if(model == "lstm"):
        TrainSize = request.GET.get("TrainSize")
        NeuronUnit = request.GET.get("NeuronUnit")
        Epochs = request.GET.get("Epochs")
        Batch_Size = request.GET.get("Batch_Size")
        LearnRate = request.GET.get("LearnRate")
        cnx = pymysql.connect(user='root', password='butyuhao',
                              host='127.0.0.1',
                              database='DeepLearningArchitecture', charset='utf8')
        cursor = cnx.cursor()
        cursor = cnx.cursor()
        sql = "select PM25, PM10, Co, No2, So2, O3 from city"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        tmpValue = []
        i = 0
        for row in results:
            i = i + 1
            tmp = []
            tmp.append(row[0])
            tmp.append(row[1])
            tmp.append(row[2])
            tmp.append(row[3])
            tmp.append(row[4])
            tmp.append(row[5])
            tmpValue.append(tmp)
        countSize = i
        cursor.close()
        cnx.close()
        # 对所有数据进行归一化
        values = tmpValue
        scaler = MinMaxScaler(feature_range=(0, 1))
        values = scaler.fit_transform(values)

        pmvalue = np.array(tmpValue)
        pmscaler = MinMaxScaler(feature_range=(0, 1))
        pmvalue = pmscaler.fit_transform(pmvalue[:, 0].reshape(-1, 1))

        # 划分测试集和训练集
        # 此处设置训练集的数量为10000，测试集的数量为1814
        deadline = int(TrainSize)
        train = values[:deadline, :]
        test = values[deadline:, :]
        train_X, train_Y = train[:, :-1], train[:, -1]
        test_X, test_Y = test[:, :-1], test[:, -1]
        # 改变形状
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        keras.backend.clear_session()
        model = Sequential()
        model.add(LSTM(int(NeuronUnit), input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        history = model.fit(train_X, train_Y, epochs=int(Epochs), batch_size=int(Batch_Size), validation_data=(test_X, test_Y), verbose=2,
                            shuffle=False)
        rms = optimizers.RMSprop(lr=float(LearnRate), rho=0.9, epsilon=1e-06)
        result = model.compile(loss="mse", optimizer=rms)

        trainLoss = 0
        testLoss = 0
        rows = []
        columns = ['number', 'TrainLoss', 'TestLoss']
        i = 0
        for loss, testloss in zip(history.history['loss'], history.history['val_loss']):
            i = i + 1
            tmp = {}
            tmp['number'] = str(i)
            tmp['TrainLoss'] = float(loss)
            tmp['TestLoss'] = float(testloss)
            rows.append(tmp)
            trainLoss = loss
            testLoss = testloss

        resultData = {}
        resultData['columns'] = columns
        resultData['rows'] = rows

        # make a prediction
        yhat = model.predict(test_X)
        # calculate RMSE
        rmse = sqrt(mean_squared_error(test_Y, yhat))

        intestY = pmscaler.inverse_transform(test_Y.reshape(-1, 1)).reshape(-1)
        inYhat = pmscaler.inverse_transform(yhat.reshape(-1, 1)).reshape(-1)

        rows2 = []
        columns2 = ['number', 'Predicted', 'Observed']
        columnsPre = ['time', '24小时', '72小时', '一周']
        rowPre = []
        j = 0
        month = 6  # 暂时写死
        day = 3
        hour = 12
        for p, o in zip(inYhat, intestY):
            j = j + 1
            tmp2 = {}
            tmp2['number'] = str(j)
            tmp2['Predicted'] = float(p)
            tmp2['Observed'] = float(o)
            rows2.append(tmp2)

            tmpPre = {}
            if (hour > 24):
                hour = 1
                day = day + 1
            sdata = str(month) + "-" + str(day) + "/" + str(hour) + ":00"
            hour = hour + 1
            tmpPre['time'] = sdata
            if(j <= 24):
                tmpPre['24小时'] = float(p)
                tmpPre['72小时'] = float(p)
                tmpPre['一周'] = float(p)
            if(j > 24 and j <= 72):
                tmpPre['24小时'] = ""
                tmpPre['72小时'] = float(p)
                tmpPre['一周'] = float(p)
            if(j > 72 and j <= 168):
                tmpPre['24小时'] = ""
                tmpPre['72小时'] = ""
                tmpPre['一周'] = float(p)

            rowPre.append(tmpPre)
            if(j == 200):
                break

        modelParameters = {}
        modelParameters['totalSize'] = countSize
        modelParameters['trainSize'] = TrainSize
        modelParameters['TestSize'] = int(countSize) - int(TrainSize)
        modelParameters['neuronUnit'] = NeuronUnit
        modelParameters['epochs'] = Epochs
        modelParameters['batch_size'] = Batch_Size
        modelParameters['learnRate'] = LearnRate
        modelParameters['Model'] = "LSTM"

        resultStatic = {}
        resultStatic['trainingCost'] = float(trainLoss)
        resultStatic['testingCost'] = testLoss
        resultStatic['RMSE'] = float(rmse)
        resultStatic['pearsonr'] = ''

        resultDatatmp = {}
        resultDatatmp['columns'] = columns2
        resultDatatmp['rows'] = rows2

        resultPrediction = {}
        resultPrediction['columns'] = columnsPre
        resultPrediction['rows'] = rowPre

        response['ResultData'] = resultDatatmp
        response['ResultData2'] = resultData
        response['resultStatic'] = resultStatic
        response['resultPrediction'] = resultPrediction
        response['modelParameters'] = modelParameters
        response['msg'] = 'success'
        response['error_num'] = 0
    return JsonResponse(response)
