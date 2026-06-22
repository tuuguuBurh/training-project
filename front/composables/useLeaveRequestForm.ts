import { useApi } from './useApi'
import { API_ENDPOINTS } from '~/constants'
import type {
  LeaveRequestCreatePayload,
  LeaveRequestFormState,
  LeaveRequestResponse,
  LeaveType,
  TeamMember,
} from '~/types/leave-request/leave-request-types'

function todayIsoDate(): string {
  return new Date().toISOString().slice(0, 10)
}

function createInitialForm(): LeaveRequestFormState {
  return {
    leaveTypeId: '',
    startDate: todayIsoDate(),
    startTime: '09:00',
    endTime: '13:00',
    description: '',
    approverIds: [],
  }
}

export function useLeaveRequestForm() {
  const api = useApi()
  const toast = useNuxtApp().$toast

  const leaveTypes = ref<LeaveType[]>([])
  const teamMembers = ref<TeamMember[]>([])
  const form = reactive<LeaveRequestFormState>(createInitialForm())
  const errors = reactive({
    leaveTypeId: false,
    approverIds: false,
    timeRange: false,
  })

  const loading = ref(false)
  const submitting = ref(false)
  const submitted = ref(false)
  const loadError = ref<string | null>(null)

  const times = Array.from({ length: 24 }, (_, h) => `${String(h).padStart(2, '0')}:00`)

  const requestedHours = computed(() => {
    const [startH, startM] = form.startTime.split(':').map(Number)
    const [endH, endM] = form.endTime.split(':').map(Number)
    const diffMinutes = endH! * 60 + endM! - (startH! * 60 + startM!)
    return diffMinutes > 0 ? Math.round((diffMinutes / 60) * 100) / 100 : 0
  })

  const timeRangeInvalid = computed(() => requestedHours.value <= 0)

  const canSubmit = computed(
    () =>
      !loading.value &&
      !submitting.value &&
      !!form.leaveTypeId &&
      form.approverIds.length > 0 &&
      !timeRangeInvalid.value,
  )

  async function loadFormData() {
    loading.value = true
    loadError.value = null

    const [typesResult, membersResult] = await Promise.all([
      api.get<LeaveType[]>(API_ENDPOINTS.LEAVE_TYPES.LIST),
      api.get<TeamMember[]>(API_ENDPOINTS.LEAVE_REQUESTS.TEAM_MEMBERS),
    ])

    if (typesResult.error || membersResult.error) {
      loadError.value = typesResult.error?.message || membersResult.error?.message || 'Мэдээлэл ачаалахад алдаа гарлаа'
      toast.error(loadError.value)
      loading.value = false
      return
    }

    leaveTypes.value = typesResult.data || []
    teamMembers.value = membersResult.data || []
    loading.value = false
  }

  function resetFormFields() {
    Object.assign(form, createInitialForm())
    errors.leaveTypeId = false
    errors.approverIds = false
    errors.timeRange = false
  }

  function validate(): boolean {
    errors.leaveTypeId = !form.leaveTypeId
    errors.approverIds = form.approverIds.length === 0
    errors.timeRange = timeRangeInvalid.value
    return !errors.leaveTypeId && !errors.approverIds && !errors.timeRange
  }

  async function submit(): Promise<boolean> {
    if (!validate()) return false

    submitting.value = true
    submitted.value = false

    const payload: LeaveRequestCreatePayload = {
      leave_type_id: form.leaveTypeId,
      start_date: form.startDate,
      start_time: `${form.startTime}:00`,
      end_time: `${form.endTime}:00`,
      description: form.description.trim() || null,
      approver_ids: form.approverIds,
    }

    const { data, error } = await api.post<LeaveRequestResponse>(
      API_ENDPOINTS.LEAVE_REQUESTS.CREATE,
      payload,
    )

    submitting.value = false

    if (error) {
      toast.error(error.message)
      return false
    }

    if (data) {
      submitted.value = true
      toast.success('Чөлөөний хүсэлт амжилттай илгээгдлээ')
      resetFormFields()
      setTimeout(() => {
        submitted.value = false
      }, 3500)
      return true
    }

    return false
  }

  onMounted(loadFormData)

  return {
    leaveTypes,
    teamMembers,
    form,
    errors,
    times,
    loading,
    submitting,
    submitted,
    loadError,
    requestedHours,
    timeRangeInvalid,
    canSubmit,
    loadFormData,
    submit,
    resetFormFields,
  }
}
