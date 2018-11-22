################# MODEL 2 #####################

#DATOS 1

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 2 3 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 4 3 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 2 3 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 4 3 model2 experiments/config_test_model2.ini

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 4 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 4 1 model2 experiments/config_test_model2.ini

#DATOS 2

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 10 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 10 4 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 50 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 50 4 1 model2 experiments/config_test_model2.ini

#DATOS 1 + DATOS 2

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 10 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 10 4 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 50 2 1 model2 experiments/config_test_model2.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 50 4 1 model2 experiments/config_test_model2.ini

