import api from "./api";

export const createCampaign = async (campaignData) => {
  const response = await api.post("/campaigns", campaignData);
  return response.data;
};

export const uploadCampaignAttachment = async (
  campaignId,
  attachment
) => {
  const formData = new FormData();

  formData.append("attachment", attachment);

  const response = await api.post(
    `/campaigns/${campaignId}/attachment`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const sendCampaign = async (campaignId) => {
  const response = await api.post(
    `/mail/send-campaign/${campaignId}`
  );

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