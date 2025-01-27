import React, { useState } from 'react';
import {
  Button,
  SafeAreaView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  View,
} from 'react-native';

const NewProduct: React.FC = () => {
  const [name, setName] = useState<string>('');
  const [manufacturer, setManufacturer] = useState<string>('');
  const [barcode, setBarcode] = useState<string>('');
  const [hasPortion, setHasPortion] = useState<boolean>(false);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Новый продукт</Text>

      <TextInput
        style={styles.input}
        placeholder="Название"
        placeholderTextColor="#888"
        value={name}
        onChangeText={setName}
      />
      <TextInput
        style={styles.input}
        placeholder="Производитель"
        placeholderTextColor="#888"
        value={manufacturer}
        onChangeText={setManufacturer}
      />
      <TextInput
        style={styles.input}
        placeholder="Штрих-код"
        placeholderTextColor="#888"
        value={barcode}
        onChangeText={setBarcode}
      />

      <View style={styles.switchContainer}>
        <Text style={styles.label}>У продукта есть порция</Text>
        <Switch value={hasPortion} onValueChange={setHasPortion} />
      </View>

      <Text style={styles.examples}>
        Примеры продуктов с порциями: йогурты, батончики, напитки в бутылках и
        т.д.
      </Text>

      <View style={styles.buttonContainer}>
        <Button title="Отменить" onPress={() => {}} color="gray" />
        <Button title="Добавить" onPress={() => {}} color="green" />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#121212', // Dark background
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 16,
  },
  input: {
    backgroundColor: '#333',
    color: 'white',
    padding: 10,
    borderRadius: 8,
    marginBottom: 12,
  },
  switchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 12,
  },
  label: {
    color: 'white',
    marginRight: 8,
  },
  examples: {
    fontSize: 12,
    color: '#aaa',
    marginBottom: 16,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
});

export default NewProduct;
