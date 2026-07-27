import api from "./api";

export const getTemplates = async () => {
  const response = await api.get("/templates/list");
  return response.data;
};

export const getTemplate = async (id) => {
  const response = await api.get(`/templates/${id}`);
  return response.data;
};
