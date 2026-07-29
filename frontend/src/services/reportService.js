import api from "./api";

export const getReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

export const getCampaignDetails = async (campaignId) => {
  const response = await api.get(
    `/reports/campaign/${campaignId}`
  );
  return response.data;
};

export const exportReports = () => {
  window.open(
    `${api.defaults.baseURL}/reports/export`,
    "_blank"
  );
};
