import api from "./api";

export const createCampaign = async (campaignData) => {
  const response = await api.post("/campaigns", campaignData);
  return response.data;
};

export const sendCampaign = async (campaignId) => {
  const response = await api.post(`/mail/send-campaign/${campaignId}`);
  return response.data;
};

export const getCampaigns = async () => {
  const response = await api.get("/campaigns");
  return response.data;
};

export const getCampaignDashboard = async () => {
  const response = await api.get("/campaigns/dashboard");
  return response.data;
};