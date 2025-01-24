import { axiosBase } from '@api';
import { CustomerProps } from '@store';

import { NutritionData, NutritionProduct, TExercises, TPlanType } from '~types';

export const createCustomer = (values: Partial<CustomerProps>) =>
  axiosBase.post('/customers', values);

export const getCustomers = () => axiosBase.get('/customers');

export const createPlan = (id: string, values: any) =>
  axiosBase.post(`/customers/${id}/training_plans`, values);

export const getExercises = () => axiosBase.get<TExercises[]>('/exercises');

export const getCustomerPlan = (id: string) =>
  axiosBase.get<TPlanType[]>(`/customers/${id}/training_plans`);

export const getCustomerPlanDetail = (id: string, planId: string) =>
  axiosBase.get<TPlanType>(`/customers/${id}/training_plans/${planId}`);

export const getDietDetails = async (date: string) => {
  const data = await axiosBase.get<NutritionData>(`/nutrition/diets/${date}`);
  return data.data;
};

export const getProductDetails = async (id: string) => {
  const data = await axiosBase.get<NutritionProduct>(
    `nutrition/products/${id}`,
  );
  return data?.data;
};

export const addProductToDiet = async (values: any) => {
  const response = await axiosBase.post('/nutrition/diets', values);
  return response.data;
};

export const getProductHistory = async () => {
  const response = await axiosBase.get<NutritionProduct[]>(
    '/nutrition/products/history/all',
  );
  return response.data;
};

export const searchProduct = async (input: string) => {
  const response = await axiosBase.get<NutritionProduct[]>(
    `/nutrition/products/lookup/${input}`,
  );
  return response.data;
};
